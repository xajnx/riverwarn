# Riverwarn: Texas River Early Warning System

`riverwarn` is a Python-based tool designed to monitor river stages in Texas and provide early warnings for potential flooding. It fetches real-time data from the USGS National Water Information System (NWIS) API, displays color-coded status updates in the terminal, and logs historical data in a SQLite database.

## Features
- Fetches current river stages for specified Texas rivers using the USGS NWIS API.
- Displays river status with color-coded output:
  - **Green**: Safe levels.
  - **Yellow**: Near flood stage (90% of flood level).
  - **Red**: Flooding.
- Stores historical stage data in a local SQLite database.
- Configurable via a `rivers.json` file for easy river management.

## Requirements
- Python 3.7+
- Dependencies (listed in `requirements.txt`):
  - `requests`
  - `colorama`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/xajnx/riverwarn.git
   cd riverwarnInstall dependencies:pip install -r requirements.txtEnsure rivers.json is configured (see below).ConfigurationEdit rivers.json to specify the rivers you want to monitor. Example:[
    {
        "name": "Brazos River at Richmond",
        "gage_id": "08114000",
        "flood_stage": 45.0
    },
    {
        "name": "Colorado River at Wharton",
        "gage_id": "08162000",
        "flood_stage": 39.0
    }
]name: River name for display.gage_id: USGS site code (find at https://waterdata.usgs.gov/tx/nwis/rt).flood_stage: Flood threshold in feet (verify with official sources).UsageRun the script:python riverwarn.pyOutput will show current stages and statuses in the terminal, and data will be saved to river_data.db.Data StorageHistorical data is stored in a SQLite database (river_data.db) with the schema:id: Auto-incrementing ID.river: River name.stage: Current stage in feet.timestamp: ISO-formatted timestamp.ContributingFeel free to submit issues or pull requests on GitHub. See Todo.md for planned enhancements.

## License
This project is open-source and available under the MIT License.

author: A.J. Nelson (xajnx)
donate: PayPal/Venmo - @therealajnelson