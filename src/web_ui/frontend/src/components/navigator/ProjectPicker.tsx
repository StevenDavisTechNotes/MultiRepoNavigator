import React, { SyntheticEvent } from 'react';
import styled from 'styled-components'
import { Dropdown } from 'semantic-ui-react'
import { IProject } from '../../models/Project.types';

interface IProps {
    projects: IProject[];
    selectedProject?: IProject;
    selectProject: (project: IProject) => void;
}

interface IState {
    isOpen: boolean;
    // optionValue: string;
}

interface IOption {
    value?: string;
}


const Container = styled.div`
`;

const StyledDropdown = styled(Dropdown)`
  &&& {
    width: 100%;
  }
`

export default class ProjectPicker extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);

        this.state = {
            isOpen: false,
            // optionValue: props.selectedProject?.id.toString() ?? '',
        };
    }

    getOptions = () => {
        let opts = this.props.projects.map(project => {
            return { text: project.logical_path, value: project.id };
        })
        return opts
    }

    changeOption = (e: SyntheticEvent, selectedOption: IOption) => {
        let new_project_id_str = selectedOption?.value;
        if (new_project_id_str == null) {
            return;
        }
        let new_project_id = parseInt(new_project_id_str);
        let new_project = this.props.projects.find(project => project.id === new_project_id);
        if (!new_project) {
            return;
        }
        this.props?.selectProject(new_project as IProject);
        // this.setState(
        //     { optionValue: new_project_id.toString() },
        // )
    }

    render() {
        return (
            <Container>
                <StyledDropdown
                    button
                    className='icon'
                    floating
                    selectOnBlur={false}
                    labeled
                    icon='dropdown'
                    options={this.getOptions()}
                    value={this.props.selectedProject?.id}
                    onChange={this.changeOption}
                    search
                    placeholder='Select Project Folder'
                />
            </Container>
        )
    }
}