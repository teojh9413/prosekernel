# Strong incident apology fixture

At 09:42 UTC, our API queue stopped processing write-demo jobs for 18 minutes. Requests were accepted but not completed. 214 jobs were delayed; 17 customers saw retries fail.

The cause was our worker autoscaler reading queue depth from a stale Redis replica. We moved queue-depth reads to primary, added a 60-second freshness check, and replayed every delayed job by 10:31 UTC.

You do not need to open a support ticket. If your job failed during the window, the dashboard now shows the replayed output and a credit on the usage page.

We should have alerted on stalled completions, not only worker health. That alert is live now.
