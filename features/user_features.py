import aiovk


def photos_info_by_user(data="urls", user_id=27196901):
    # ToDo: Remove after normal auth
    app_secret = "x49X1eyoU1BTPrFsBBVx"
    app_id = 7150578
    app_service = "dbfc62d1dbfc62d1dbfc62d140db917923ddbfcdbfc62d186725cfca26ef9526763372e"
    with aiovk.ImplicitSession("89851301115", "evvdatascience", app_id, "groups,friends,photos, albums") as session:
        api = aiovk.API(session)

        photo_infos = []
        albums_request = api.photos.getAlbums(owner_id=user_id)
        albums = await albums_request
        album_ids = [album_info["id"] for album_info in albums.get("items")]
        for album_id_cs in album_ids:
            photos_by_album = await api.photos.get(album_id=album_id_cs)
            photo_infos += [{"url": photo_info["photo_604"], "date": photo_info['date']} for photo_info in
                            photos_by_album.get("items")]

    if data is None:
        return photo_infos
    elif data == "urls":
        return [photo_info["url"] for photo_info in photo_infos]
    elif data == "full":
        return photo_infos
