# Email types
EMAIL_ACTIVATION = "activation"
EMAIL_PASSWORD_RESET = "password_reset"


# Roles
ROLE_USER = "user"
ROLE_ADMIN = "admin"

# Permissions
PERMISSION_EXAMPLE = "permission:example"

# Role permissions
ROLES = {
    ROLE_USER: [],
    ROLE_ADMIN: [
        PERMISSION_EXAMPLE,
    ],
}

# Misc
SEARCH_RESULT_LIMIT = 12
