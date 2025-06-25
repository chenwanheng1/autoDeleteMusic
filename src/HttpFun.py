import json
import FileOperation as fileOp
#登录
def login(http_client,endpoint,username,password):
    post_json_response = http_client.post(
        endpoint=endpoint,
        json_data={
            "username": username,
            "password": password
        }
    )
    token = ""
    nid = ""
    if post_json_response:
        token = post_json_response["token"]
        nid = post_json_response["id"]

    return token,nid

#获取歌单列表，找到【不喜欢】歌单，返回id
def get_play_list(http_client,endpoint,start,end,token,nid):
    get_response = http_client.get(
        endpoint=endpoint,
        params={"_start": start, "_end=": end, "_order=": "AES", "_sort": "name"},
        headers={'x-nd-authorization': 'Bearer ' + token, 'x-nd-client-unique-id': nid}
    )
    play_list_id = None
    if get_response:
        for elem in get_response:
            if elem["name"] == "不喜欢":
                play_list_id = elem["id"]
    return play_list_id

#根据歌单id查询歌单列表，返回歌曲id列表
def get_delete_list(http_client, endpoint,list_id,start,end, token, nid):
    get_response = http_client.get(
        endpoint=endpoint,
        params={"_start": start, "_end=": end, "_order=": "AES", "_sort": "id","playlist_id": list_id},
        headers={'x-nd-authorization': 'Bearer ' + token, 'x-nd-client-unique-id': nid}
    )
    delete_list = []
    if get_response:
        for elem in get_response:
            path = elem["path"]
            delete_list.append(fileOp.extract_filename(path))
    return delete_list


def get_miss_list(http_client,endpoint,start,end,token,nid):
    get_response = http_client.get(
        endpoint=endpoint,
        params={"_start": start, "_end=": end, "_order=": "DESC", "_sort": "updated_at"},
        headers={'x-nd-authorization': 'Bearer ' + token, 'x-nd-client-unique-id': nid}
    )
    miss_list = []
    if get_response:
        for elem in get_response:
            title = elem["id"]
            miss_list.append(title)
    return miss_list


def delete_miss_file(http_client, endpoint, miss_list,token,nid):
    if len(miss_list)>0:
        endpoint += "?"
        for index, element in enumerate(miss_list):
            if index < len(miss_list) - 1:
                endpoint += "id=" + element + "&"
            else:
                endpoint += "id=" + element

    get_response = http_client.delete(
        endpoint=endpoint,
        headers={'x-nd-authorization': 'Bearer ' + token, 'x-nd-client-unique-id': nid}
    )
    print("hello")