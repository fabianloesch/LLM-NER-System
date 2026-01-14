export function validateCorpus(corpus) {
  const errors = []

  try {
    // Parse JSON
    const parsed = JSON.parse(corpus)

    // Check if it's an array
    if (!Array.isArray(parsed)) {
      errors.push('Der Input muss ein JSON-Array sein')
      return errors
    }

    // Validate each entry
    parsed.forEach((entry, index) => {
      // Check required fields
      if (!entry.hasOwnProperty('id')) {
        errors.push(`Eintrag ${index}: Fehlendes Feld 'id'`)
      } else if (typeof entry.id !== 'number') {
        errors.push(`Eintrag ${index}: 'id' muss eine Zahl sein`)
      }

      if (!entry.hasOwnProperty('text')) {
        errors.push(`Eintrag ${index}: Fehlendes Feld 'text'`)
      } else if (typeof entry.text !== 'string') {
        errors.push(`Eintrag ${index}: 'text' muss ein String sein`)
      }

      if (!entry.hasOwnProperty('label')) {
        errors.push(`Eintrag ${index}: Fehlendes Feld 'label'`)
      } else if (!Array.isArray(entry.label)) {
        errors.push(`Eintrag ${index}: 'label' muss ein Array sein`)
      } else {
        // Validate label entries
        entry.label.forEach((labelEntry, labelIndex) => {
          if (!Array.isArray(labelEntry) || labelEntry.length !== 3) {
            errors.push(
              `Eintrag ${index}, Label ${labelIndex}: Muss ein Array mit 3 Elementen sein [start, end, type]`,
            )
          } else {
            const [start, end, type] = labelEntry

            if (typeof start !== 'number') {
              errors.push(
                `Eintrag ${index}, Label ${labelIndex}: Start-Position muss eine Zahl sein`,
              )
            }

            if (typeof end !== 'number') {
              errors.push(`Eintrag ${index}, Label ${labelIndex}: End-Position muss eine Zahl sein`)
            }

            if (typeof type !== 'string') {
              errors.push(`Eintrag ${index}, Label ${labelIndex}: Type muss ein String sein`)
            }

            // Check if positions are valid
            if (typeof start === 'number' && typeof end === 'number' && start >= end) {
              errors.push(
                `Eintrag ${index}, Label ${labelIndex}: Start-Position muss kleiner als End-Position sein`,
              )
            }

            // Check if positions are within text bounds
            if (entry.text && typeof start === 'number' && typeof end === 'number') {
              if (start < 0 || end > entry.text.length) {
                errors.push(
                  `Eintrag ${index}, Label ${labelIndex}: Positionen außerhalb des Text-Bereichs`,
                )
              }
            }
          }
        })
      }
    })
  } catch (e) {
    errors.push(`Ungültiges JSON-Format: ${e.message}`)
  }

  return errors
}
