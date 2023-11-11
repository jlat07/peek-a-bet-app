The documentation snippet you've provided is a guide on how to set up real-time listeners using Supabase's real-time capabilities. Supabase leverages PostgreSQL's replication feature to broadcast changes to clients in real-time.

Let's incorporate this real-time functionality into your Streamlit app. To do this, you'll need to set up a real-time subscription in your app, then update the Streamlit interface whenever new data is inserted into the table you're monitoring. You'll likely want to perform these updates on the frontend using JavaScript, as Streamlit runs on the server side and doesn't directly support real-time WebSockets.

However, since Streamlit doesn't natively support WebSocket connections, you'll have to use a workaround. You can use Streamlit's server-side capabilities to periodically poll for changes or use a Streamlit component to handle WebSocket connections on the client-side.

Below is a conceptual example using Streamlit's custom component feature to listen to Supabase's real-time updates and then trigger a re-run of Streamlit's script to update the UI:

```python
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Set up the connection to Supabase.
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# Supabase listener for new inserts. This should be set up using a custom component
# that interfaces with the Supabase JavaScript client.
# The component would handle establishing the connection and subscribing to updates.
# It would then trigger Streamlit to re-run when new data is available.

# Use an autorefresh component to periodically check for updates.
# This is a temporary measure to simulate real-time updates.
# The interval is set to 5000 ms (5 seconds).
# You would remove this once your custom component is set up to handle WebSocket connections.
refresh_interval = 5000  # milliseconds
last_update_time = st_autorefresh(interval=refresh_interval, key="data_update")

# Placeholder for real-time data updates
realtime_data = st.empty()

# Your main app logic here
def display_data():
    # Query data from Supabase
    data = supabase.table('games').select('*').order('date', ascending=False).execute()
    # Display data in Streamlit
    realtime_data.dataframe(data)

display_data()

# Assuming you have a custom component that updates `realtime_data`,
# the display would automatically update when `display_data()` is called again.
```

This example uses the `streamlit-autorefresh` component as a placeholder to simulate real-time updates by refreshing the page every 5 seconds. Once you've implemented the real WebSocket handling in a custom component that interfaces with the Supabase real-time functionality, you would remove the autorefresh part.

Creating a custom component that interfaces with the Supabase real-time API would require knowledge of both JavaScript and the Streamlit component API, as it would need to:

1. Establish the WebSocket connection to Supabase.
2. Listen to the relevant events from the database.
3. Communicate back to the Streamlit app to update the UI.

This is an advanced implementation and may require a fair amount of custom coding to get right. The custom component would essentially act as a bridge between Streamlit's Python backend and the Supabase real-time functionality on the frontend.