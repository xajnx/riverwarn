# Todo

## Immediate Tasks
- [ ] Verify flood stages in `rivers.json` against official USGS/NWS data.
- [ ] Expand `rivers.json` with more Texas rivers and their gage IDs.
- [ ] Test script with edge cases (e.g., missing data, API downtime).

## Planned Enhancements
- [ ] Add a continuous monitoring mode with a configurable refresh interval (e.g., every 15 minutes).
- [ ] Implement email or SMS alerts for flood conditions using `smtplib` or a service like Twilio.
- [ ] Create a simple web dashboard with `Flask` or `FastAPI` to visualize river statuses.
- [ ] Add support for additional states beyond Texas by modifying the API query.
- [ ] Include historical data analysis (e.g., trends or averages) using SQLite queries.
- [ ] Enhance terminal output with `rich` for tables or progress bars.

## Long-Term Goals
- [ ] Integrate with multiple data sources (e.g., NOAA API alongside USGS) for redundancy.
- [ ] Package as a standalone executable with `PyInstaller` for easier distribution.
- [ ] Add unit tests with `pytest` to ensure reliability.
- [ ] Document API limitations (e.g., rate limits) and handle them gracefully.