import { ApplicationInsights } from '@microsoft/applicationinsights-web'
import { config } from '@/config'

let appInsights: ApplicationInsights | null = null

function getAppInsights() {
  if (!appInsights) {
    appInsights = new ApplicationInsights({
      config: {
        connectionString: `InstrumentationKey=${config.applicationInsights}`,
        enableAutoRouteTracking: true,
      },
    })
    appInsights.loadAppInsights()
    appInsights.addTelemetryInitializer((envelope) => {
      if (envelope.tags) envelope.tags['ai.cloud.role'] = config.title
    })
    appInsights.trackEvent({ name: `${config.title} - app started` })
  }
  return appInsights
}

export function useLogger() {
  const insights = getAppInsights()

  function logEvent(name: string, properties?: Record<string, unknown>) {
    insights.trackEvent({ name: `${config.title} - ${name}`, properties })
  }

  return { logEvent }
}
