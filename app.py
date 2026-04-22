import json
import uuid
from datetime import date, datetime
from pathlib import Path

import streamlit as st

DATA_FILE = Path("requests_data.json")

STATUS_OPTIONS = ["New", "In Progress", "Waiting", "Completed"]
PRIORITY_OPTIONS = ["Low", "Medium", "High"]
REQUEST_TYPE_OPTIONS = ["File", "Response", "Follow-up", "Other"]


def load_requests():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_requests(requests):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(requests, f, indent=2)


def format_date(date_str):
    if not date_str:
        return "No due date"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
    except ValueError:
        return date_str


def is_overdue(date_str, status):
    if not date_str or status == "Completed":
        return False
    try:
        due = datetime.strptime(date_str, "%Y-%m-%d").date()
        return due < date.today()
    except ValueError:
        return False


def get_people_options(requests):
    names = set()
    for r in requests:
        if r.get("requester"):
            names.add(r["requester"])
        if r.get("assigned_to"):
            names.add(r["assigned_to"])
    if not names:
        names = {"Alex", "Jordan", "Taylor"}
    return sorted(names)


def apply_filters(requests, selected_person, view_mode, status_filter, priority_filter, type_filter, search_query):
    filtered = requests[:]

    if selected_person != "All":
        if view_mode == "Sent":
            filtered = [r for r in filtered if r.get("requester") == selected_person]
        elif view_mode == "Received":
            filtered = [r for r in filtered if r.get("assigned_to") == selected_person]

    if status_filter != "All":
        filtered = [r for r in filtered if r.get("status") == status_filter]

    if priority_filter != "All":
        filtered = [r for r in filtered if r.get("priority") == priority_filter]

    if type_filter != "All":
        filtered = [r for r in filtered if r.get("request_type") == type_filter]

    if search_query:
        q = search_query.lower()
        filtered = [
            r for r in filtered
            if q in r.get("title", "").lower()
            or q in r.get("description", "").lower()
            or q in r.get("requester", "").lower()
            or q in r.get("assigned_to", "").lower()
        ]

    return filtered


def create_request(title, request_type, description, requester, assigned_to, priority, due_date):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "id": str(uuid.uuid4())[:8],
        "title": title.strip(),
        "request_type": request_type,
        "description": description.strip(),
        "requester": requester.strip(),
        "assigned_to": assigned_to.strip(),
        "priority": priority,
        "status": "New",
        "due_date": due_date.isoformat() if due_date else "",
        "response_note": "",
        "delivered_item": "",
        "created_at": now,
        "updated_at": now,
    }


st.set_page_config(page_title="Team Request Tracker", layout="wide")
st.title("Team Request Tracker")
st.caption("A one-page app to submit, track, and fulfill team requests without Slack fog.")

if "requests" not in st.session_state:
    st.session_state.requests = load_requests()

requests = st.session_state.requests

# Top metrics
total_count = len(requests)
open_count = len([r for r in requests if r["status"] != "Completed"])
in_progress_count = len([r for r in requests if r["status"] == "In Progress"])
completed_count = len([r for r in requests if r["status"] == "Completed"])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total", total_count)
m2.metric("Open", open_count)
m3.metric("In Progress", in_progress_count)
m4.metric("Completed", completed_count)

st.divider()

left, right = st.columns([1, 1.4])

with left:
    st.subheader("Submit New Request")

    with st.form("new_request_form", clear_on_submit=True):
        title = st.text_input("Title *")
        request_type = st.selectbox("Request Type", REQUEST_TYPE_OPTIONS)
        description = st.text_area("Description *", height=100)
        requester = st.text_input("Requester *")
        assigned_to = st.text_input("Assigned To *")
        priority = st.selectbox("Priority", PRIORITY_OPTIONS, index=1)
        due_date = st.date_input("Due Date", value=None)

        submitted = st.form_submit_button("Create Request")

        if submitted:
            if not title.strip() or not description.strip() or not requester.strip() or not assigned_to.strip():
                st.error("Please fill in Title, Description, Requester, and Assigned To.")
            else:
                new_request = create_request(
                    title, request_type, description, requester, assigned_to, priority, due_date
                )
                st.session_state.requests.append(new_request)
                save_requests(st.session_state.requests)
                st.success("Request created.")
                st.rerun()

    st.subheader("Filters")
    people_options = ["All"] + get_people_options(requests)
    selected_person = st.selectbox("Person", people_options)
    view_mode = st.radio("View", ["All", "Sent", "Received"], horizontal=True)
    status_filter = st.selectbox("Status", ["All"] + STATUS_OPTIONS)
    priority_filter = st.selectbox("Priority", ["All"] + PRIORITY_OPTIONS)
    type_filter = st.selectbox("Request Type", ["All"] + REQUEST_TYPE_OPTIONS)
    search_query = st.text_input("Search")

with right:
    st.subheader("Requests")

    filtered_requests = apply_filters(
        requests,
        selected_person,
        view_mode,
        status_filter,
        priority_filter,
        type_filter,
        search_query,
    )

    if not filtered_requests:
        st.info("No requests match the current filters.")
    else:
        # newest first
        filtered_requests = sorted(filtered_requests, key=lambda r: r["created_at"], reverse=True)

        for request in filtered_requests:
            overdue = is_overdue(request.get("due_date", ""), request.get("status", ""))

            priority_badge = {
                "High": "🔴 High",
                "Medium": "🟠 Medium",
                "Low": "🟢 Low",
            }.get(request["priority"], request["priority"])

            status_badge = {
                "New": "🆕 New",
                "In Progress": "⏳ In Progress",
                "Waiting": "⏸️ Waiting",
                "Completed": "✅ Completed",
            }.get(request["status"], request["status"])

            title_line = f"{request['title']}  |  {status_badge}  |  {priority_badge}"
            if overdue:
                title_line += "  |  ⚠️ Overdue"

            with st.expander(title_line):
                c1, c2 = st.columns([1.2, 1])

                with c1:
                    st.write(f"**Request ID:** {request['id']}")
                    st.write(f"**Type:** {request['request_type']}")
                    st.write(f"**Requester:** {request['requester']}")
                    st.write(f"**Assigned To:** {request['assigned_to']}")
                    st.write(f"**Due Date:** {format_date(request['due_date'])}")
                    st.write(f"**Created:** {request['created_at']}")
                    st.write("**Description:**")
                    st.write(request["description"] or "_No description_")

                    if request.get("response_note"):
                        st.write("**Response Note:**")
                        st.write(request["response_note"])

                    if request.get("delivered_item"):
                        st.write(f"**Delivered Item / Response:**** {request['delivered_item']}")

                with c2:
                    st.write("**Update Request**")
                    update_key = request["id"]

                    new_status = st.selectbox(
                        "Status",
                        STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(request["status"]),
                        key=f"status_{update_key}",
                    )
                    new_assignee = st.text_input(
                        "Assigned To",
                        value=request["assigned_to"],
                        key=f"assignee_{update_key}",
                    )
                    new_priority = st.selectbox(
                        "Priority",
                        PRIORITY_OPTIONS,
                        index=PRIORITY_OPTIONS.index(request["priority"]),
                        key=f"priority_{update_key}",
                    )

                    current_due = None
                    if request["due_date"]:
                        try:
                            current_due = datetime.strptime(request["due_date"], "%Y-%m-%d").date()
                        except ValueError:
                            current_due = None

                    new_due_date = st.date_input(
                        "Due Date",
                        value=current_due,
                        key=f"due_{update_key}",
                    )
                    new_response_note = st.text_area(
                        "Response Note",
                        value=request.get("response_note", ""),
                        key=f"response_{update_key}",
                        height=100,
                    )
                    new_delivered_item = st.text_input(
                        "Delivered File / Response",
                        value=request.get("delivered_item", ""),
                        key=f"delivered_{update_key}",
                    )

                    col_a, col_b = st.columns(2)

                    with col_a:
                        if st.button("Save Update", key=f"save_{update_key}", use_container_width=True):
                            request["status"] = new_status
                            request["assigned_to"] = new_assignee.strip()
                            request["priority"] = new_priority
                            request["due_date"] = new_due_date.isoformat() if new_due_date else ""
                            request["response_note"] = new_response_note.strip()
                            request["delivered_item"] = new_delivered_item.strip()
                            request["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            save_requests(st.session_state.requests)
                            st.success("Request updated.")
                            st.rerun()

                    with col_b:
                        if st.button("Delete", key=f"delete_{update_key}", use_container_width=True):
                            st.session_state.requests = [
                                r for r in st.session_state.requests if r["id"] != request["id"]
                            ]
                            save_requests(st.session_state.requests)
                            st.warning("Request deleted.")
                            st.rerun()
