import streamlit as st

from utils.theme import load_theme
from database.auth import (
    get_all_users,
    create_user,
    update_user,
    delete_user,
    reset_password,
    enable_user,
    disable_user,
    make_admin,
    remove_admin,
)

# =====================================================
# Helper Functions
# =====================================================

def get_statistics(users):
    """Calculate dashboard statistics."""

    total = len(users)
    admins = sum(user["is_admin"] for user in users)
    active = sum(user["is_active"] for user in users)
    disabled = total - active

    return total, admins, active, disabled


def filter_users(users, search, role_filter, status_filter):
    """Filter users based on search and dropdown filters."""

    filtered = []

    for user in users:

        # -----------------------------
        # Search
        # -----------------------------

        if search:

            query = search.lower()

            if (
                query not in user["username"].lower()
                and query not in user["full_name"].lower()
                and query not in user["email"].lower()
            ):
                continue

        # -----------------------------
        # Role
        # -----------------------------

        if role_filter != "All":

            if role_filter == "Admin" and not user["is_admin"]:
                continue

            if role_filter == "User" and user["is_admin"]:
                continue

        # -----------------------------
        # Status
        # -----------------------------

        if status_filter != "All":

            if status_filter == "Active" and not user["is_active"]:
                continue

            if status_filter == "Disabled" and user["is_active"]:
                continue

        filtered.append(user)

    return filtered


def role_badge(user):

    if user["is_admin"]:
        return "Administrator"

    return "User"


def status_badge(user):

    if user["is_active"]:
        return "🟢 Active"

    return "🔴 Disabled"

# =====================================================
# Add User Dialog
# =====================================================

@st.dialog("Add User", width="large")
def open_add_user():

    st.subheader("Create New User")

    col1, col2 = st.columns(2)

    with col1:

        username = st.text_input(
            "Username",
            key="add_username",
        )

        full_name = st.text_input(
            "Full Name",
            key="add_fullname",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="add_password",
        )

    with col2:

        email = st.text_input(
            "Email",
            key="add_email",
        )

        role = st.selectbox(
            "Role",
            ["USER", "ADMIN"],
            key="add_role",
        )

        active = st.checkbox(
            "Active Account",
            value=True,
            key="add_active",
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        if st.button(
            "Create User",
            type="primary",
            use_container_width=True,
            key="create_user_btn",
        ):

            if not all([
                username.strip(),
                full_name.strip(),
                email.strip(),
                password.strip(),
            ]):
                st.error("All fields are required.")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters.")
                return

            success, message = create_user(
                username=username.strip(),
                full_name=full_name.strip(),
                email=email.strip(),
                password=password,
                role=role,
                is_admin=1 if role == "ADMIN" else 0,
            )

            if success:

                if not active:

                    users = get_all_users()

                    new_user = next(
                        (
                            u
                            for u in users
                            if u["username"] == username.strip()
                        ),
                        None,
                    )

                    if new_user:
                        disable_user(new_user["id"])

                st.toast("✅ User created successfully.")
                st.rerun()

            else:
                st.error(message)

    with right:

        if st.button(
            "Cancel",
            use_container_width=True,
            key="cancel_add_user",
        ):
            return

# =====================================================
# Edit User Dialog
# =====================================================

@st.dialog("Edit User", width="large")
def open_edit_user(user):

    st.subheader(user["username"])

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Username",
            value=user["username"],
            disabled=True,
            key=f"edit_username_{user['id']}",
        )

        full_name = st.text_input(
            "Full Name",
            value=user["full_name"],
            key=f"edit_fullname_{user['id']}",
        )

    with col2:

        email = st.text_input(
            "Email",
            value=user["email"],
            key=f"edit_email_{user['id']}",
        )

        role = st.selectbox(
            "Role",
            ["USER", "ADMIN"],
            index=1 if user["is_admin"] else 0,
            key=f"edit_role_{user['id']}",
        )

    active = st.checkbox(
        "Active Account",
        value=bool(user["is_active"]),
        key=f"edit_active_{user['id']}",
    )

    st.divider()

    left, middle, right = st.columns(3)

    # -------------------------------------------------
    # Save Changes
    # -------------------------------------------------

    with left:

        if st.button(
            "Save Changes",
            type="primary",
            use_container_width=True,
            key=f"save_{user['id']}",
        ):

            if not full_name.strip() or not email.strip():
                st.error("Name and Email are required.")
                return

            current_user = st.session_state.get("user")

            is_current_user = (
                current_user is not None
                and current_user["id"] == user["id"]
            )

            if is_current_user:

                if role != "ADMIN":
                    st.error("You cannot remove your own administrator privileges.")
                    return

                if not active:
                    st.error("You cannot disable your own account.")
                    return

            update_user(
                user_id=user["id"],
                full_name=full_name.strip(),
                email=email.strip(),
                role=role,
                is_admin=1 if role == "ADMIN" else 0,
                is_active=1 if active else 0,
            )

            make_admin(user["id"]) if role == "ADMIN" else remove_admin(user["id"])

            enable_user(user["id"]) if active else disable_user(user["id"])

            st.toast("✅ User updated successfully.")
            st.rerun()

    # -------------------------------------------------
    # Reset Password
    # -------------------------------------------------

    with middle:

        if st.button(
            "Reset Password",
            key=f"reset_{user['id']}",
            use_container_width=True,
        ):
            open_reset_password_dialog(user)

    # -------------------------------------------------
    # Delete User
    # -------------------------------------------------

    with right:

        if st.button(
            "Delete User",
            key=f"delete_btn_{user['id']}",
            use_container_width=True,
        ):
            open_delete_user_dialog(user)

# =====================================================
# Reset Password Dialog
# =====================================================

@st.dialog("Reset Password", width="medium")
def open_reset_password_dialog(user):

    st.subheader("Reset Password")

    st.caption(
        f"Changing password for **{user['username']}**"
    )

    st.write("")

    new_password = st.text_input(
        "New Password",
        type="password",
        key=f"new_password_{user['id']}",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key=f"confirm_password_{user['id']}",
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        if st.button(
            "Update Password",
            type="primary",
            use_container_width=True,
            key=f"update_password_{user['id']}",
        ):

            if not new_password.strip():
                st.error("Password cannot be empty.")
                return

            if len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")
                return

            if new_password != confirm_password:
                st.error("Passwords do not match.")
                return

            try:

                reset_password(
                    user["id"],
                    new_password,
                )

                st.toast("Password updated successfully.")
                st.rerun()

            except Exception as e:
                st.error(str(e))

    with right:

        if st.button(
            "Cancel",
            use_container_width=True,
            key=f"cancel_reset_{user['id']}",
        ):
            return

# =====================================================
# Delete User Dialog
# =====================================================

@st.dialog("Delete User", width="medium")
def open_delete_user_dialog(user):

    st.error("This action cannot be undone.")

    st.write(
        f"Are you sure you want to permanently delete "
        f"**{user['full_name']} (@{user['username']})**?"
    )

    st.divider()

    left, right = st.columns(2)

    # -------------------------------------------------
    # Confirm Delete
    # -------------------------------------------------

    with left:

        if st.button(
            "Delete User",
            type="primary",
            key=f"confirm_delete_{user['id']}",
            use_container_width=True,
        ):

            current_user = st.session_state.get("user")

            if (
                current_user is not None
                and current_user["id"] == user["id"]
            ):
                st.error("You cannot delete your own account.")
                return

            delete_user(user["id"])

            st.toast("🗑 User deleted successfully.")

            st.rerun()

    # -------------------------------------------------
    # Cancel
    # -------------------------------------------------

    with right:

        if st.button(
            "Cancel",
            key=f"cancel_delete_{user['id']}",
            use_container_width=True,
        ):
            return

# =====================================================
# Main Page
# =====================================================

def show_user_management():

    # -------------------------------------------------
    # Theme
    # -------------------------------------------------

    load_theme()

    # -------------------------------------------------
    # Load Users
    # -------------------------------------------------

    users = get_all_users()

    # -------------------------------------------------
    # Header
    # -------------------------------------------------

    header_left, header_right = st.columns([5, 1])

    with header_left:

        st.title("User Management")
        st.caption("Manage users, roles and permissions.")

    with header_right:

        st.write("")
        st.write("")

        if st.button(
            "Add User",
            use_container_width=True,
            type="primary",
        ):
            open_add_user()

    st.divider()

    # -------------------------------------------------
    # KPI Cards
    # -------------------------------------------------

    total, admins, active, disabled = get_statistics(users)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="Total Users",
            value=total,
        )

    with c2:
        st.metric(
            label="Administrators",
            value=admins,
        )

    with c3:
        st.metric(
            label="Active Users",
            value=active,
        )

    with c4:
        st.metric(
            label="Disabled Users",
            value=disabled,
        )

    st.write("")

    # -------------------------------------------------
    # Search & Filters
    # -------------------------------------------------

    search_col, role_col, status_col = st.columns([4, 1, 1])

    with search_col:

        search = st.text_input(
            "Search Users",
            placeholder="🔍 Search by username, name or email...",
            label_visibility="collapsed",
        )

    with role_col:

        role_filter = st.selectbox(
            "Role",
            [
                "All",
                "Admin",
                "User",
            ],
        )

    with status_col:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Active",
                "Disabled",
            ],
        )

    st.write("")

    # -------------------------------------------------
    # Filter Data
    # -------------------------------------------------

    filtered_users = filter_users(
        users,
        search,
        role_filter,
        status_filter,
    )

    # -------------------------------------------------
    # Empty State
    # -------------------------------------------------

    if len(filtered_users) == 0:

        st.info("No users found matching your search.")

        return

    # -------------------------------------------------
    # User Cards
    # -------------------------------------------------

    for user in filtered_users:

        with st.container(border=True):

            left, right = st.columns([6, 1])

            with left:

                st.markdown(
                    f"### 👤 {user['full_name']}"
                )

                st.caption(
                    f"@{user['username']}"
                )

                st.markdown(
                    f"{user['email']}"
                )

                st.markdown(
                    role_badge(user)
                )

                st.markdown(
                    status_badge(user)
                )

                last_login = user["last_login"]

                if not last_login:
                    last_login = "Never"

                st.caption(
                    f"Last Login: {last_login}"
                )

            with right:

                st.write("")
                st.write("")
                st.write("")

                if st.button(
                    "Edit Profile",
                    key=f"edit_{user['id']}",
                    use_container_width=True,
                ):
                    open_edit_user(user)

        st.write("")
