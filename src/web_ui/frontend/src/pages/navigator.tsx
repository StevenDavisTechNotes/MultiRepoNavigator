// Filename - pages/navigator.js
import _ from 'lodash';
import createLogger from 'logging';
import React from 'react';
import { Container, Input } from 'semantic-ui-react';
import { fetchAllProjectFolders, updateProjectFolderLastUsed } from '../apis/JotunProjectFolders';
import ProjectPicker from '../components/navigator/ProjectPicker';
import { IProject } from '../models/Project.types';
import styled from 'styled-components';
import FileList from '../components/navigator/FileList';
import { ISourceCodeFile } from '../models/SourceCodeFile.types';
import { fetchSourceCodeUnderPath } from '../apis/JotunSourceCodeFile';

const logger = createLogger('navigator_page');

interface IProps {
}

interface IState {
    files: ISourceCodeFile[];
    projects: IProject[];
    sourceCodeSearchPath: string;
    selectedProject?: IProject;
}


const StyledInput = styled(Input)`
  &&& > input {
    padding-left: 8px;
    padding-right: 8px;
    width: 200;
  }
`

export default class NavigatorPage extends React.Component<IProps, IState> {
    private debouncePromise: NodeJS.Timeout | undefined;

    constructor(props: IProps) {
        super(props);

        this.state = {
            files: [],
            projects: [],
            sourceCodeSearchPath: "",
        };

        this.debouncePromise = undefined;
    }

    componentDidMount() {
        logger.info('Starting to download Project Folder data')
        fetchAllProjectFolders()
            .then((projects: IProject[]) => {
                projects = _.orderBy(projects, ['last_used', 'id'], ['desc', 'asc']);
                logger.info(`Received ${projects.length} projects`)
                let selectedProject = _.first(projects);
                this.setState({ projects, selectedProject });
            });
    }


    onSelectProject = (project: IProject) => {
        logger.info(`Selected ${project.logical_path} project`)
        if (project.id === this.state.selectedProject?.id) {
            return;
        }
        let new_project = { ...project, last_used: new Date() };
        let new_projects = [new_project, ...this.state.projects.filter(p => p.id !== project.id)];
        updateProjectFolderLastUsed(new_project.id, new_project.last_used);
        this.setState({
            files: [],
            selectedProject: new_project,
            projects: new_projects,
            sourceCodeSearchPath: "",
        });
        fetchSourceCodeUnderPath("", new_project)
            .then(([project_folder, source_code_files]) => {
                this.setState({ files: source_code_files });
            })

    }


    onSourceCodeSearch(event: React.SyntheticEvent<HTMLInputElement>) {
        let sourceCodeSearchPath = event.currentTarget.value;
        this.setState({ sourceCodeSearchPath, files: [] });
        clearTimeout(this.debouncePromise);
        if (this.state.selectedProject != null) {
            this.debouncePromise = setTimeout(() => {
                fetchSourceCodeUnderPath(sourceCodeSearchPath, this.state.selectedProject)
                    .then(([project_folder, source_code_files]) => {
                        this.setState({ files: source_code_files });
                    })
            }, 25);
        }
    }


    render() {
        let { files, projects, selectedProject } = this.state;
        const projectPickerProps = {
            projects,
            selectedProject,
            selectProject: this.onSelectProject,
        }
        const fileListProps = {
            files,
            project: selectedProject,
        }
        return (
            <Container>
                <h1>Navigator Dashboard</h1>
                <ProjectPicker {...projectPickerProps} />
                <StyledInput
                    fluid
                    id="source_code_search"
                    placeholder='File Search...'
                    onChange={(e: React.SyntheticEvent<HTMLInputElement>) => this.onSourceCodeSearch(e)}
                    value={this.state.sourceCodeSearchPath}
                />
                <FileList {...fileListProps} />
            </Container>
        )
    }
}
