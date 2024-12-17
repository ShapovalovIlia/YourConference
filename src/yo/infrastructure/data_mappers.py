from application import User


def user_mapper(data: list[tuple[int, str, str]]) -> list["User"]:
    ans = []
    for one_user_data in data:
        user = User(one_user_data[0], one_user_data[1], one_user_data[2])
        ans.append(user)
    return ans
