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


async def group_txt_photos_by_user(user_id):
    session = aiovk.TokenSession(access_token='dbfc62d1dbfc62d1dbfc62d140db917923ddbfcdbfc62d186725cfca26ef9526763372e')
    api = aiovk.API(session)
    groups_info = await api.users.getSubscriptions(user_id=user_id)
    groups_ids = groups_info['groups']['items']
    groups_info_parsed = await api.groups.getById(group_ids=",".join([str(each) for each in groups_ids]), fields = "description")
    text_info_groups = [{"group_id":each["id"], "name":each["name"], "description":each["description"]} for each in groups_info_parsed]
    for group in text_info_groups:
            group['post_photos'] = await get_post_urls(group['group_id'], api)
            time.sleep(1)
    await session.close()
    return text_info_groups


async def photos_info_by_user(data="urls", user_id=317799):
    photo_infos = []
    session = aiovk.TokenSession(access_token='dbfc62d1dbfc62d1dbfc62d140db917923ddbfcdbfc62d186725cfca26ef9526763372e')
    api = aiovk.API(session)
    albums_request = api.photos.getAlbums(owner_id=user_id)
    albums = await albums_request
    album_ids = [album_info["id"] for album_info in albums.get("items")]
    for album_id_cs in album_ids:
        photos_by_album = await api.photos.get(owner_id=user_id, album_id=album_id_cs)
        photo_infos += [{"url": photo_info["photo_604"], "date": photo_info['date']} for photo_info in
                        photos_by_album.get("items")]
    await session.close()
    return [photo['url'] for photo in photo_infos]
