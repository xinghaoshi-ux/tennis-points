export function usePolling(
  fn: () => Promise<boolean>,
  interval: number = 3000,
  maxAttempts: number = 60
) {
  let timer: ReturnType<typeof setInterval> | null = null
  let attempts = 0

  const start = () => {
    stop()
    attempts = 0
    timer = setInterval(async () => {
      attempts++
      try {
        const done = await fn()
        if (done || attempts >= maxAttempts) {
          stop()
        }
      } catch {
        stop()
      }
    }, interval)
  }

  const stop = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  return { start, stop }
}
