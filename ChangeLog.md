---

### `ChangeLog.md`
```markdown
# ChangeLog

## Version 2.0 (March 27, 2025)
- **Rewritten Core Functionality**:
  - Replaced HTML scraping of NOAA NWS (`water.weather.gov`) with USGS NWIS API (`waterservices.usgs.gov`) for reliable JSON data.
  - Switched from `urllib.request` and `BeautifulSoup` to `requests` for HTTP requests.
- **Improved Structure**:
  - Modularized code into functions (`fetch_river_stage`, `display_status`, etc.).
  - Added error handling for network failures and invalid data.
- **Configuration**:
  - Replaced `tx.txt` with `rivers.json` for river metadata (name, gage ID, flood stage).
- **Data Persistence**:
  - Added SQLite database (`river_data.db`) to log historical river stages.
- **Dependencies**:
  - Updated to use `requests` and `colorama`; removed `bs4`.
- **Output**:
  - Retained color-coded terminal output with `colorama`.

## Version 1.0 (circa 2018)
- Initial release.
- Scraped river data from NOAA NWS HTML pages.
- Used `urllib.request` and `BeautifulSoup` for data retrieval.
- Displayed color-coded status in terminal with `colorama`.
- Saved data to a plain text file (`river_data.txt`).
- Focused solely on Texas rivers listed in `tx.txt`.