from pytube import Playlist, YouTube
from multiprocessing import Pool
import os
from time import sleep


pl = Playlist(input('Digite o link da playlist: '))
enumerated_list = [[i, url] for i, url in enumerate(pl.video_urls)]
folder_destination = pl.title.replace(" ", "-")


def download_video(item_enumerated_url):

    yt_link = YouTube(item_enumerated_url[1])
    print(f'Download started - {yt_link.title}')
    video1 = yt_link.streams.get_highest_resolution()
    video1.download(f"{folder_destination}/",
                    filename=f"{item_enumerated_url[0]}-{yt_link.title.replace('|','-').replace('?', '')}.mp4")


def update_not_downloaded(p):

    dir_path = f"{folder_destination}/"
    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        for f in filenames:
            f_path = os.path.join(dirpath, f)
            f_size = os.path.getsize(f_path)  # bytes
            f_size_kb = f_size/1024  # kbytes
            sleep(0.1)
            index = int(f.split('-')[0])
            print(index, f_size_kb)
            if f_size_kb == 0:
                yt2 = YouTube(p.video_urls[index])
                print(f'Download started - {yt2.title}')
                video2 = yt2.streams.filter(res='720p').first()
                video2.download(f"{folder_destination}/",
                                filename=f"{index}-{yt2.title.replace('|','-').replace('?','')}.mp4")
            print(f'Download completed!')


def check_missing_items(url_list):

    for url in url_list:
        yt3 = YouTube(url[1])
        print(f'Download started - {yt3.title}')
        video = yt3.streams.filter(res='720p').first()
        video.download(f"{folder_destination}/",
                       filename=f"{url[0]}-{yt3.title.replace('|', '-').replace('?', '')}.mp4")


if __name__ == '__main__':

    with Pool(4) as pool:
        pool.map(download_video, enumerated_list)

    update_not_downloaded(pl)
    check_missing_items(enumerated_list)
