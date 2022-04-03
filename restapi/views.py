def get_user_info(request):
    user = getattr(request, "user", None)

    if user:
        return {
            "id": user.id,
            "username": user.username
        }
    else:
        return {

        }