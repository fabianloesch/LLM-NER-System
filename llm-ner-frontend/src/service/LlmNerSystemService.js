import apiClient from './LlmNerSystemApi'

export const apiService = {
  async getAllUsages() {
    const response = await apiClient.get('/modelRuns')
    return response.data
  },

  async getModelRunById(modelRunId) {
    const response = await apiClient.get(`/modelRun/${modelRunId}`)
    return response.data
  },

  async createModelRun(modelRun) {
    const response = await apiClient.post('/modelRun', modelRun)
    return response.data
  },

  async getAllEvaluations() {
    const response = await apiClient.get('/modelEvaluations')
    return response.data
  },

  async getEvaluationById(modelRunId) {
    const response = await apiClient.get(`/modelEvaluation/${modelRunId}`)
    return response.data
  },

  async createEvaluation(modelRun) {
    const response = await apiClient.post('/modelEvaluation', modelRun)
    return response.data
  },

  async getAvailableModels() {
    const response = await apiClient.get('/availableModels')
    return response.data
  },
}
