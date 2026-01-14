export function transformEvaluationData(metricsData) {
  if (metricsData == {} || metricsData == null) return []

  const result = []
  const metrics = ['precision', 'recall', 'f1_score']

  // Iterate through each model
  for (const [modelName, modelData] of Object.entries(metricsData)) {
    // For each KPI (precision, recall, f1_score)
    metrics.forEach((metric) => {
      const row = {
        model: modelName,
        metric: metric,
        overall: modelData.overall[metric],
      }

      // Add all entity class values
      if (modelData.entityClassLevel) {
        for (const [entityClass, metrics] of Object.entries(modelData.entityClassLevel)) {
          row[entityClass] = metrics[metric]
        }
      }

      result.push(row)
    })
  }

  return result
}
