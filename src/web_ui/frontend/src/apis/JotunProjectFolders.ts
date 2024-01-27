import axios from 'axios';
import { chain } from 'lodash';
import { IProject } from '../models/Project.types';

const JOTUN_API_URL = 'http://127.0.0.1:4059'

export interface ApiProject {
    id: number;
    last_used: string;
    logical_path: string;
    app_name: string;
}

export function convertApiProjectToProject(apiProject: ApiProject): IProject {
    return {
        id: apiProject.id,
        last_used: new Date(apiProject.last_used),
        logical_path: apiProject.logical_path,
        app_name: apiProject.app_name,
    };
}

export function fetchAllProjectFolders(): Promise<IProject[]> {
    return axios.get(`${JOTUN_API_URL}/project_folder`)
        .then(res =>
            chain(res.data as ApiProject[])
                .map(convertApiProjectToProject)
                .orderBy(['last_used', 'id'], ['desc', 'asc'])
                .value()
        );
}

export function updateProjectFolderLastUsed(project_id: number, last_used: Date): Promise<boolean> {
    return (
        axios.patch(`${JOTUN_API_URL}/project_folder/${project_id}`, {
            id: project_id,
            last_used,  // : last_used.toISOString(),
        }).then(res => true)
    );
}