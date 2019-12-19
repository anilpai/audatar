import request from 'superagent';

export function getSearchResults(searchTerm, appPrefix) {
    return new Promise((resolve) => {
        request.get(`${appPrefix}/dataset/?s=${searchTerm}`)
        .set('Authorization', 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc0FkbWluIjp0cnVlLCJ1c2VybmFtZSI6ImFwYWkiLCJleHAiOjE1NDE3MzMzOTN9.6c6tLAOT_P4X295xiYzr_eS21bhhlt3EjiSglnBFJBM')
        .end((error, response) => {
            if (error) {
                return resolve({error});
            }
            return resolve(response.body);
        });
    });
}

export default {getSearchResults};
