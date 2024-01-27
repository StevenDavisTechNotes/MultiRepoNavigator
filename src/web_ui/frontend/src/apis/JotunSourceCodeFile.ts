import axios from 'axios';
import { chain } from 'lodash';
import { ISourceCodeFile } from '../models/SourceCodeFile.types';
import { convertApiProjectToProject } from './JotunProjectFolders';
import { IProject } from '../models/Project.types';

const JOTUN_API_URL = 'http://127.0.0.1:4059'

export function convertApiSourceCodeFileToSourceCodeFile(logical_path: string): ISourceCodeFile {
    return {
        logical_path: logical_path,
    };
}

export function fetchSourceCodeUnderPath(
    source_code_path: string,
    selected_project_folder?: IProject,
): Promise<[IProject, ISourceCodeFile[]]> {
    const params = new URLSearchParams()
    params.append('abs_or_rel_source_path', source_code_path)
    if (selected_project_folder != null) {
        params.append('selected_project_folder', selected_project_folder.logical_path)
    }
    return axios.get(`${JOTUN_API_URL}/source_code/list_code_files`, { params })
        .then(res => {
            let { project_folder, code_file_paths } = res.data;
            let refined_files = chain(code_file_paths as string[])
                .map(convertApiSourceCodeFileToSourceCodeFile)
                .value()
            let refined_project = convertApiProjectToProject(project_folder)
            return [project_folder, refined_files];
        });
}
