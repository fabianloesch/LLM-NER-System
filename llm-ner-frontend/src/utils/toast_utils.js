function showSuccess(toast, details) {
  toast.add({
    severity: 'success',
    summary: 'Success Message',
    detail: details,
    life: 5000,
  })
}

function showError(toast, details) {
  toast.add({
    severity: 'error',
    summary: 'Error Message',
    detail: details,
    life: 5000,
  })
}

// Handle validation events from child
export function handleSuccess(toast, message) {
  showSuccess(toast, message)
}

export function handleErrors(toast, errors) {
  showError(toast, errors.join(' '))
}
