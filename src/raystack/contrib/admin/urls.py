import os

from fastapi import APIRouter, Request

from raystack.conf import settings
from raystack.shortcuts import render_template

from fastapi import Depends, HTTPException, status
import jwt
from jwt import PyJWTError as JWTError

from fastapi.security import OAuth2PasswordBearer

from raystack.contrib.auth.accounts.decorators import login_required

from raystack.contrib.auth.users.models import UserModel
from raystack.contrib.auth.groups.models import GroupModel
from raystack.contrib.auth.groups.forms import GroupCreateForm


router = APIRouter()


def url_for(endpoint, **kwargs):
    """
    Function for generating URL based on endpoint and additional parameters.
    In this case, endpoint is ignored as we only use filename.
    """
    path = f"/{endpoint}"

    if not kwargs:
        return path
    
    for key, value in kwargs.items():
        path += f"/{value}"
    
    return path


@router.get("/users", response_model=None)
@login_required(["user_auth"])
async def users_view(request: Request):
    users = await UserModel.objects.all().execute_all()  # type: ignore

    return render_template(request=request, template_name="admin/users.html", context={
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Users",
        "config": request.app.settings,
        "users": users,
    })


@router.get("/groups", response_model=None)
@login_required(["user_auth"])
async def groups_view(request: Request):
    groups = await GroupModel.objects.all().execute()  # type: ignore

    return render_template(request=request, template_name="admin/groups.html", context={
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Groups",
        "config": request.app.settings,
        "groups": groups,
    })


@router.get("/", response_model=None)
@login_required(["user_auth"])
async def dashboard_view(request: Request):
    """Dashboard view with statistics"""
    # Get statistics
    total_users = await UserModel.objects.count()
    total_groups = await GroupModel.objects.count()
    
    # Mock statistics for now - in real app these would come from actual data
    stats = {
        "total_users": total_users,
        "new_users_today": 5,  # Mock data
        "total_groups": total_groups,
        "active_groups": total_groups,  # Mock data
        "online_users": 12,  # Mock data
        "system_status": "Online"  # Mock data
    }
    
    # Get recent users for activity feed
    recent_users = await UserModel.objects.all().execute()
    # Limit to 5 users for display
    recent_users = recent_users[:5] if recent_users else []
    
    # Mock recent activities data
    recent_activities = [
        {
            "user": {"name": "Admin User", "email": "admin@example.com"},
            "action": "User Login",
            "description": "Successful authentication",
            "timestamp": "2 minutes ago",
            "status": "Completed"
        },
        {
            "user": {"name": "John Doe", "email": "john@example.com"},
            "action": "Profile Update",
            "description": "Updated personal information",
            "timestamp": "15 minutes ago",
            "status": "Completed"
        },
        {
            "user": {"name": "Jane Smith", "email": "jane@example.com"},
            "action": "Group Creation",
            "description": "Created new user group",
            "timestamp": "1 hour ago",
            "status": "Completed"
        }
    ]
    
    # Mock system information
    system_info = {
        "version": "1.0.0",
        "uptime": "2 days, 5 hours",
        "memory_usage": 45,
        "cpu_usage": 23
    }
    
    return render_template(request=request, template_name="admin/dashboard.html", context={
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Dashboard",
        "config": request.app.settings,
        "stats": stats,
        "recent_users": recent_users,
        "recent_activities": recent_activities,
        "system_info": system_info,
    })

@router.get("/logs", response_model=None)
@login_required(["user_auth"])
async def logs_view(request: Request):
    """System logs view"""
    # Mock logs data - in real app this would come from actual log files
    from datetime import datetime
    logs = [
        {
            "timestamp": datetime(2024, 1, 15, 10, 30, 15),
            "level": "INFO", 
            "message": "User login successful", 
            "user": {"name": "admin"},
            "module": "auth",
            "function": "login",
            "details": "User authenticated successfully",
            "ip_address": "192.168.1.100"
        },
        {
            "timestamp": datetime(2024, 1, 15, 10, 25, 42),
            "level": "WARNING", 
            "message": "Failed login attempt", 
            "user": {"name": "unknown"},
            "module": "auth",
            "function": "login",
            "details": "Invalid credentials provided",
            "ip_address": "192.168.1.101"
        },
        {
            "timestamp": datetime(2024, 1, 15, 10, 20, 18),
            "level": "INFO", 
            "message": "Database backup completed", 
            "user": {"name": "system"},
            "module": "backup",
            "function": "create_backup",
            "details": "Backup file created successfully",
            "ip_address": "127.0.0.1"
        },
        {
            "timestamp": datetime(2024, 1, 15, 10, 15, 33),
            "level": "ERROR", 
            "message": "Connection timeout", 
            "user": {"name": "system"},
            "module": "database",
            "function": "connect",
            "details": "Database connection failed after 30 seconds",
            "ip_address": "127.0.0.1"
        },
        {
            "timestamp": datetime(2024, 1, 15, 10, 10, 55),
            "level": "INFO", 
            "message": "New user registered", 
            "user": {"name": "john_doe"},
            "module": "registration",
            "function": "register_user",
            "details": "User account created successfully",
            "ip_address": "192.168.1.102"
        },
    ]
    
    # Calculate log statistics
    stats = {
        "info_count": len([log for log in logs if log["level"] == "INFO"]),
        "warning_count": len([log for log in logs if log["level"] == "WARNING"]),
        "error_count": len([log for log in logs if log["level"] == "ERROR"]),
        "total_count": len(logs)
    }
    
    return render_template(request=request, template_name="admin/logs.html", context={
        "url_for": url_for,
        "parent": "Admin",
        "segment": "System Logs",
        "config": request.app.settings,
        "logs": logs,
        "stats": stats,
    })


@router.get("/settings", response_model=None)
@login_required(["user_auth"])
async def settings_view(request: Request):
    """System settings view"""
    # Mock settings data - in real app this would come from actual settings
    settings_data = {
        "site_name": "Raystack Admin",
        "site_description": "Administrative interface for Raystack",
        "maintenance_mode": False,
        "debug_mode": True,
        "max_users": 1000,
        "session_timeout": 3600,
        "email_notifications": True,
        "backup_frequency": "daily",
    }
    
    return render_template(request=request, template_name="admin/settings.html", context={
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Settings",
        "config": request.app.settings,
        "settings": settings_data,
    })

@router.get("/users/edit/{user_id}", response_model=None)
@login_required(["user_auth"])
async def user_edit_view(request: Request, user_id: int):
    user = await UserModel.objects.filter(id=user_id).first()
    groups = await GroupModel.objects.all().execute()
    return render_template(request=request, template_name="admin/user_edit.html", context={
        "user": user,
        "groups": groups,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Edit User",
        "config": request.app.settings,
    })

@router.post("/users/edit/{user_id}", response_model=None)
@login_required(["user_auth"])
async def user_edit_post(request: Request, user_id: int):
    form = await request.form()
    user = await UserModel.objects.filter(id=user_id).first()
    if user:
        user.name = form.get("name")
        user.age = int(form.get("age"))
        user.email = form.get("email")
        user.organization = form.get("organization")
        group_id = int(form.get("group_id"))
        user.group = group_id
        await user.save()
    return render_template(request=request, template_name="admin/user_edit.html", context={
        "user": user,
        "groups": await GroupModel.objects.all().execute(),
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Edit User",
        "config": request.app.settings,
        "success": True
    })

@router.get("/groups/edit/{group_id}", response_model=None)
@login_required(["user_auth"])
async def group_edit_view(request: Request, group_id: int):
    group = await GroupModel.objects.filter(id=group_id).first()
    return render_template(request=request, template_name="admin/group_edit.html", context={
        "group": group,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Edit Group",
        "config": request.app.settings,
    })

@router.post("/groups/edit/{group_id}", response_model=None)
@login_required(["user_auth"])
async def group_edit_post(request: Request, group_id: int):
    form = await request.form()
    group = await GroupModel.objects.filter(id=group_id).first()
    if group:
        group.name = form.get("name")
        group.description = form.get("description")
        await group.save()
    return render_template(request=request, template_name="admin/group_edit.html", context={
        "group": group,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Edit Group",
        "config": request.app.settings,
        "success": True
    })

# --- User Create ---
@router.get("/users/create", response_model=None)
@login_required(["user_auth"])
async def user_create_view(request: Request):
    groups = await GroupModel.objects.all().execute()
    return render_template(request=request, template_name="admin/user_create.html", context={
        "groups": groups,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Create User",
        "config": request.app.settings,
    })

@router.post("/users/create", response_model=None)
@login_required(["user_auth"])
async def user_create_post(request: Request):
    form = await request.form()
    user = UserModel(
        name=form.get("name"),
        age=int(form.get("age")),
        email=form.get("email"),
        password_hash="",  # Set password later or generate
        group=int(form.get("group_id")),
        organization=form.get("organization")
    )
    await user.save()
    return render_template(request=request, template_name="admin/user_create.html", context={
        "groups": await GroupModel.objects.all().execute(),
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Create User",
        "config": request.app.settings,
        "success": True
    })

# --- User Delete ---
@router.get("/users/delete/{user_id}", response_model=None)
@login_required(["user_auth"])
async def user_delete_confirm(request: Request, user_id: int):
    user = await UserModel.objects.filter(id=user_id).first()
    return render_template(request=request, template_name="admin/user_delete.html", context={
        "user": user,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Delete User",
        "config": request.app.settings,
    })

@router.post("/users/delete/{user_id}", response_model=None)
@login_required(["user_auth"])
async def user_delete_post(request: Request, user_id: int):
    user = await UserModel.objects.filter(id=user_id).first()
    if user:
        await user.delete()
    # Redirect to users list after deletion
    return render_template(request=request, template_name="admin/user_delete.html", context={
        "deleted": True,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Delete User",
        "config": request.app.settings,
    })

# --- Group Create ---
@router.get("/groups/create", response_model=None)
@login_required(["user_auth"])
async def group_create_view(request: Request):
    form = GroupCreateForm()
    return render_template(request=request, template_name="admin/group_create.html", context={
        "form": form,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Create Group",
        "config": request.app.settings,
    })

@router.post("/groups/create", response_model=None)
@login_required(["user_auth"])
async def group_create_post(request: Request):
    data = await request.form()
    form = GroupCreateForm(data)
    if form.is_valid():
        group = GroupModel(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"]
        )
        await group.save()
        return render_template(request=request, template_name="admin/group_create.html", context={
            "form": GroupCreateForm(),
            "url_for": url_for,
            "parent": "Admin",
            "segment": "Create Group",
            "config": request.app.settings,
            "success": True
        })
    return render_template(request=request, template_name="admin/group_create.html", context={
        "form": form,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Create Group",
        "config": request.app.settings,
        "errors": "Please fix the errors in the form."
    })

# --- Group Delete ---
@router.get("/groups/delete/{group_id}", response_model=None)
@login_required(["user_auth"])
async def group_delete_confirm(request: Request, group_id: int):
    group = await GroupModel.objects.filter(id=group_id).first()
    return render_template(request=request, template_name="admin/group_delete.html", context={
        "group": group,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Delete Group",
        "config": request.app.settings,
    })

@router.post("/groups/delete/{group_id}", response_model=None)
@login_required(["user_auth"])
async def group_delete_post(request: Request, group_id: int):
    group = await GroupModel.objects.filter(id=group_id).first()
    if group:
        await group.delete()
    return render_template(request=request, template_name="admin/group_delete.html", context={
        "deleted": True,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "Delete Group",
        "config": request.app.settings,
    })


# --- User View ---
@router.get("/users/view/{user_id}", response_model=None)
@login_required(["user_auth"])
async def user_view(request: Request, user_id: int):
    user = await UserModel.objects.filter(id=user_id).first()
    return render_template(request=request, template_name="admin/user_view.html", context={
        "user": user,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "View User",
        "config": request.app.settings,
    })


# --- Group View ---
@router.get("/groups/view/{group_id}", response_model=None)
@login_required(["user_auth"])
async def group_view(request: Request, group_id: int):
    group = await GroupModel.objects.filter(id=group_id).first()
    # Get users in this group
    users_in_group = await UserModel.objects.filter(group=group_id).execute()
    return render_template(request=request, template_name="admin/group_view.html", context={
        "group": group,
        "users_in_group": users_in_group,
        "url_for": url_for,
        "parent": "Admin",
        "segment": "View Group",
        "config": request.app.settings,
    })
