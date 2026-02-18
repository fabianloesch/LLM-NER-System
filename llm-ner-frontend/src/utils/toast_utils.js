import { useToast } from 'primevue/usetoast'

export function useToastUtils() {
  const toast = useToast()

  return {
    handleSuccess(message) {
      toast.add({ severity: 'success', summary: 'Erfolg', detail: message, life: 5000 })
    },
    handleErrors(errors) {
      toast.add({ severity: 'error', summary: 'Fehler', detail: errors.join(' '), life: 5000 })
    },
  }
}
