# Cash Register Simulator

This is a simple Flask-based API that simulates a cash register for Joy's cafés. It provides a route to generate fake transaction data for a given store and time range.

## How to Run

**Start the server**

   In your terminal, navigate to this directory and run:

   ```sh
   python app.py
   ```

   Or, use your IDE's play button in the cash-register/app.py file.
   
   The app will run on [http://localhost:5001](http://localhost:5001).

## API Usage

### `GET /transactions`

Simulate a random list of transactions for a store within a given time range.

**Query Parameters:**
- `store_id` (required): The ID of the store (e.g., `1` or `2`)
- `start_time` (required): Start of the time range (ISO format, e.g., `2024-06-01T10:00:00`)
- `end_time` (required): End of the time range (ISO format, e.g., `2024-06-01T10:10:00`)

**Example Request:**
```
http://localhost:5001/transactions?store_id=1&start_time=2024-06-01T10:00:00&end_time=2024-06-01T10:10:00
```


## Notes

- The number of transactions returned is random (between 0 and 20).
- Each transaction includes a random timestamp within the requested range and a random amount between $2.00 and $20.00.

---
