import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/travel"

st.set_page_config(page_title="TripMate AI", page_icon="✈️", layout="wide")
st.title("✈️ TripMate AI")
st.caption("Multi-agent travel planner · LangGraph + FastAPI")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Session")
    st.write(f"Thread: `{st.session_state.thread_id or 'new'}`")
    if st.button("New chat"):
        st.session_state.thread_id = None
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        details = msg.get("details")
        if details:
            tab_flights, tab_hotels, tab_itinerary = st.tabs(
                ["Flights", "Hotels", "Itinerary"]
            )
            tab_flights.markdown(details["flight_results"])
            tab_hotels.markdown(details["hotel_results"])
            tab_itinerary.markdown(details["itinerary"])
            st.caption(f"LLM calls: {details['llm_calls']}")

prompt = st.chat_input("e.g. 3 day trip to Goa from Delhi under 20000 INR")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agents are planning your trip..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"message": prompt, "thread_id": st.session_state.thread_id},
                    timeout=300,
                )
                data = resp.json()
            except requests.exceptions.RequestException as e:
                data = {"success": False, "error": f"Could not reach the API: {e}"}
            except ValueError:
                data = {"success": False, "error": "API returned invalid JSON."}

    if data.get("success"):
        st.session_state.thread_id = data["thread_id"]
        st.session_state.messages.append({
            "role": "assistant",
            "content": data["answer"],
            "details": {
                "flight_results": data["flight_results"],
                "hotel_results": data["hotel_results"],
                "itinerary": data["itinerary"],
                "llm_calls": data["llm_calls"],
            },
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"⚠️ {data.get('error', 'Unknown error')}",
        })
    st.rerun()