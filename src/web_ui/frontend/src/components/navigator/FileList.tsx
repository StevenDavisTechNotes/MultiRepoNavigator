import React from 'react';
import { IProject } from '../../models/Project.types';
import { ISourceCodeFile } from '../../models/SourceCodeFile.types';

interface IProps {
    project?: IProject;
    files: ISourceCodeFile[];
}

interface IState {
}

export default class FileList extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);

        this.state = {
        };
    }


    render() {
        return (
            <ul>
                {
                    this.props.files
                        .map(file =>
                            <li key={file.logical_path}>{file.logical_path}</li>
                        )
                }
            </ul>
        )
    }
}