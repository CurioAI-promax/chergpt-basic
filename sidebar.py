import streamlit as st
from app.chatlog.chatlog_handler import delete_all_chatlogs, export_chat_logs_to_csv, drop_chatlog_table
from app.instructions.instructions_handler import get_latest_instructions, update_instructions
from app.db.database_connection import  drop_instructions_table, get_app_description, update_app_description
custominstructions_area_height = 300
app_description = get_app_description()

def setup_sidebar():
    with st.sidebar:
        st.title("Settings")
        with st.expander("🔑 Admin login"):
            admin_password = st.text_input("Educators only", type="password", key="admin_password")
            if admin_password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state["is_admin"] = True
                st.success("Authenticated as Admin")
            elif admin_password:  
                st.error("Incorrect password")
                st.session_state["is_admin"] = False

    if st.session_state.get("is_admin", False):
        with st.sidebar:
            # Check if the user is an admin to provide editing capability
            # Provide a text area for admins to edit the app description
            with st.expander("⚙️ Edit description"):
                editable_description = st.text_area("This amends text below title", value=app_description, key="app_description")
                # Button to save the updated app description
                if st.button("Update description", key="save_app_description"):
                    # Update the app description in the database
                    update_app_description(editable_description)
                    st.success("App description updated successfully")

            with st.expander("📝 Custom instructions"):
                st.session_state['existing_instructions'] = get_latest_instructions()
                custom_instructions = st.text_area("Edit and save to guide interactions", value=st.session_state['existing_instructions'], height=custominstructions_area_height)

                if st.button("Save Instructions"):
                    update_instructions(custom_instructions)
                    st.success("Instructions updated successfully")
                    st.rerun()

            with st.expander("💬 Chatlog and insights"):
                csv_data = export_chat_logs_to_csv()
                if csv_data:
                    st.download_button(label="Download Chat Logs", data=csv_data, file_name='chat_logs.csv', mime='text/csv',)
                if st.button("Delete All Chat Logs"):
                    delete_all_chatlogs()
            with st.expander("⚠️ Warning: destructive actions"):
                if st.button("Drop chatlog table"):
                    drop_chatlog_table()
                    st.success("Chatlog table dropped")
                    st.rerun()
                if st.button("Drop instructions table"):
                    drop_instructions_table()
                    st.success("Instructions table dropped")
                    st.rerun()


