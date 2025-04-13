from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TYER, TRCK, APIC, ID3NoHeaderError
from mutagen.mp3 import MP3
import os

mp3_tags_frame = ('                      ___                _     _\n'
                  '                    / _  )              ( ) _ ( )_)\n'
                  '   ___ ___   _ _   (_)_) |      __     _| |(_)|  _)   _    _ __\n'
                  ' /  _   _  \(  _ \  _(_ (     / __ \ / _  || || |   / _ \ (  __)\n'
                  ' | ( ) ( ) || (_) )( )_) |   (  ___/( (_| || || |_ ( (_) )| |   \n'
                  ' (() ( ) (_)|  __/  \____)    )\___) ) _ _)( ))\__) \ __/ (()   \n'
                  ' (_) /(     | |              (__)   (__)   /((__)   /(    (_)   \n'
                  '    (__)    (_)                           (__)     (__)          by tg: @newzelland_tg\n')
print(mp3_tags_frame)
def edit_mp3_tags_interactive():
    file_path = input("Введите путь к MP3 файлу: ").strip('"')

    if not os.path.exists(file_path):
        print("Файл не найден!")
        return

    print("\nВведите новые значения (оставьте пустым, чтобы не изменять):")
    title = input("Название: ")
    artist = input("Исполнитель: ")
    album = input("Альбом: ")
    genre = input("Жанр: ")
    year = input("Год: ")
    track = input("Номер трека: ")
    cover_path = input("Путь к изображению обложки (оставьте пустым, чтобы не изменять): ").strip('"')

    try:
        # Пытаемся загрузить существующие теги
        try:
            audio = ID3(file_path)
        except ID3NoHeaderError:
            # Если тегов нет, создаем новый объект
            audio = ID3()
            print("Файл не содержал ID3-тегов. Будет создан новый набор тегов.")

        # Обновляем текстовые теги
        if title:
            audio["TIT2"] = TIT2(encoding=3, text=title)
        if artist:
            audio["TPE1"] = TPE1(encoding=3, text=artist)
        if album:
            audio["TALB"] = TALB(encoding=3, text=album)
        if genre:
            audio["TCON"] = TCON(encoding=3, text=genre)
        if year:
            audio["TYER"] = TYER(encoding=3, text=year)
        if track:
            audio["TRCK"] = TRCK(encoding=3, text=track)

        # Обновляем обложку
        if cover_path:
            if os.path.exists(cover_path):
                try:
                    # Определяем MIME-тип по расширению файла
                    ext = os.path.splitext(cover_path)[1].lower()
                    mime_type = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'

                    with open(cover_path, 'rb') as cover_file:
                        # Удаляем старые обложки, если они есть
                        audio.delall("APIC")
                        audio["APIC"] = APIC(
                            encoding=3,
                            mime=mime_type,
                            type=3,  # 3 - обложка альбома
                            desc='Cover',
                            data=cover_file.read()
                        )
                    print("Обложка успешно обновлена!")
                except Exception as e:
                    print(f"Ошибка при обновлении обложки: {e}")
            else:
                print("Файл обложки не найден!")

        # Сохраняем теги в файл
        audio.save(file_path)
        print("Теги успешно обновлены!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    edit_mp3_tags_interactive()