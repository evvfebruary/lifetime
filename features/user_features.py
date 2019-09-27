import time
import aiovk


async def get_post_urls(group_id, vk_api):
    post_urls = []
    try:
        group_wallpost = await vk_api.wall.get(owner_id=group_id)
    except Exception:
        return []
    for post in group_wallpost['items']:
        attachments = post.get("attachments")
        if attachments is not None:
            for attachment in attachments:
                if attachment.get('type') == "photo":
                    post_urls.append(attachment['photo']["photo_604"])
    return post_urls


async def group_txt_photos_by_user(user_id=27196901):
    # ToDo: Remove after normal auth
    app_secret = "x49X1eyoU1BTPrFsBBVx"
    app_id = 7150578
    app_service = "dbfc62d1dbfc62d1dbfc62d140db917923ddbfcdbfc62d186725cfca26ef9526763372e"
    session = aiovk.ImplicitSession("89851301115", "evvdatascience", app_id, "groups,friends,photos, albums")
    api = aiovk.API(session)
    # ToDo: Remove after normal auth
    groups_info = await api.users.getSubscriptions(user_ids=user_id)
    groups_ids = groups_info['groups']['items']
    groups_info_parsed = await api.groups.getById(group_ids=",".join([str(each) for each in groups_ids]), fields = "description")
    text_info_groups = [{"group_id": each["id"], "name":each["name"], "description":each["description"]} for each in groups_info_parsed]
    for group in text_info_groups:
            group['post_photos'] = await get_post_urls(group['group_id'], api)
            time.sleep(1)
    return text_info_groups


async def photos_info_by_user(data="urls", user_id=27196901):
    # ToDo: Remove after normal auth
    app_secret = "x49X1eyoU1BTPrFsBBVx"
    app_id = 7150578
    app_service = "dbfc62d1dbfc62d1dbfc62d140db917923ddbfcdbfc62d186725cfca26ef9526763372e"
    session = aiovk.ImplicitSession("89851301115", "evvdatascience", app_id, "groups,friends,photos, albums")
    api = aiovk.API(session)
    # ToDo: Remove after normal auth
    photo_infos = []
    albums_request = api.photos.getAlbums(owner_id=user_id)
    albums = await albums_request
    album_ids = [album_info["id"] for album_info in albums.get("items")]
    for album_id_cs in album_ids:
        photos_by_album = await api.photos.get(album_id=album_id_cs)
        photo_infos += [{"url": photo_info["photo_604"], "date": photo_info['date']} for photo_info in
                        photos_by_album.get("items")]

    print(photo_infos)
    await session.close()
    if data is None:
        return photo_infos
    elif data == "urls":
        return [photo_info["url"] for photo_info in photo_infos]
    elif data == "full":
        return photo_infos
