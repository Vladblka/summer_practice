from tkinter import *
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime
import numpy as np
import os
import cv2


class App:
    """Класс, реализующий приложение."""
    @classmethod
    def create(cls):
        """
        Создает основное окно и параметры, используемые в других функция
        """
        root = Tk()
        root.title("GigaProgram")
        root.geometry("800x600")
        root.resizable(False, False)

        cls.root = root
        cls.image = None
        cls.width_val = None
        cls.height_val = None
        cls.cap = None
        cls.is_camera_active = False
        cls.b_color_user = None
        cls.g_color_user = None
        cls.r_color_user = None
        cls.x_coord = None
        cls.y_coord = None
        cls.radius = None

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=True)

        image_frame = Frame(main_frame)
        image_frame.pack(fill=BOTH, expand=True, pady=20)

        cls.img_label = Label(image_frame)
        cls.img_label.pack(fill=BOTH, expand=True)

        button_frame = Frame(main_frame)
        button_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        cls.choice_btn = Button(
            button_frame,
            text="Выбрать изображение",
            command=cls.open_image
            )
        cls.choice_btn.pack(side=LEFT, padx=5)

        cls.photo_btn = Button(
            button_frame,
            text="Сделать снимок",
            command=cls.start_camera
            )
        cls.photo_btn.pack(side=LEFT, padx=5)

        cls.change_btn = Button(
            button_frame,
            text="Изменить размер",
            command=lambda: messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите изображение"
                )
            )
        cls.change_btn.pack(side=LEFT, padx=5)

        cls.bright_btn = Button(
            button_frame,
            text="Изменить яркость",
            command=lambda: messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите изображение"
                )
            )
        cls.bright_btn.pack(side=LEFT, padx=5)

        cls.draw_btn = Button(
            button_frame,
            text="Нарисовать круг",
            command=lambda: messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите изображение"
                )
            )
        cls.draw_btn.pack(side=LEFT, padx=5)

        cls.save_btn = Button(
            button_frame,
            text="Сохранить",
            command=lambda: messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите изображение"
                )
            )
        cls.save_btn.pack(side=LEFT, padx=5)

        if cls.image is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "ava.png")
            screen = Image.open(image_path)
            max_size = (750, 500)
            if screen.width > max_size[0] or screen.height > max_size[1]:
                screen.thumbnail(max_size, Image.LANCZOS)

            photo = ImageTk.PhotoImage(screen)

            cls.img_label.config(image=photo)
            cls.img_label.image = photo

        root.mainloop()

    @classmethod
    def open_image(cls):
        """Открывает изображение, выбранное пользователем"""

        cls.stop_camera()

        filetypes = [("Изображения", "*.jpg *.png")]

        try:
            file_path = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=filetypes
            )

            if not file_path:
                return

            ext = os.path.splitext(file_path)[1].lower()
            if ext not in ['.jpg', '.png']:
                messagebox.showerror(
                    "Ошибка",
                    "Неправильный формат файла. Выберите JPG или PNG."
                    )
                return

            image = Image.open(file_path)
            cls.image = image

            max_size = (750, 500)
            if image.width > max_size[0] or image.height > max_size[1]:
                image.thumbnail(max_size, Image.LANCZOS)

            photo = ImageTk.PhotoImage(image)

            cls.img_label.config(image=photo)
            cls.img_label.image = photo

            cls.change_btn.config(command=lambda: cls.change_size_window())
            cls.bright_btn.config(command=lambda: cls.bright_window())
            cls.draw_btn.config(command=lambda: cls.draw_circle_window())
            cls.save_btn.config(command=lambda: cls.save_image())

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось загрузить изображение: {str(e)}"
                )

    @classmethod
    def stop_camera(cls):
        """Останавливает работу камеры"""
        if cls.is_camera_active:
            cls.is_camera_active = False
            cls.cap.release()
            cls.photo_btn.config(
                text="Сделать снимок",
                command=lambda: cls.start_camera()
                )

            cls.img_label.config(image="")

    @classmethod
    def start_camera(cls):
        """Начинает работу камеры"""
        try:
            cls.cap = cv2.VideoCapture(0)
            if not cls.cap.isOpened():
                messagebox.showerror("Ошибка", "Не удалось открыть камеру.")
                return
            cls.is_camera_active = True
            cls.photo_btn.config(
                text="Сфотографировать",
                command=lambda: cls.capture_photo()
                )
            cls.update_camera_frame()
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось запустить камеру: {str(e)}"
                )

    @classmethod
    def update_camera_frame(cls):
        """Обновляет кадр камеры"""
        if cls.is_camera_active:
            ret, frame = cls.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)

                max_size = (750, 500)
                if image.width > max_size[0] or image.height > max_size[1]:
                    image.thumbnail(max_size, Image.LANCZOS)

                photo = ImageTk.PhotoImage(image=image)
                cls.img_label.config(image=photo)
                cls.img_label.image = photo

                cls.img_label.after(10, cls.update_camera_frame)

    @classmethod
    def capture_photo(cls):
        """Делает снимок"""
        if cls.is_camera_active:
            ret, frame = cls.cap.read()
            if ret:
                try:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame)

                    cls.image = image

                    max_size = (750, 500)
                    if image.width > max_size[0] or image.height > max_size[1]:
                        image.thumbnail(max_size, Image.LANCZOS)

                    cls.save_image()

                    photo = ImageTk.PhotoImage(image=image)
                    cls.img_label.config(image=photo)
                    cls.img_label.image = photo

                except Exception as e:
                    messagebox.showerror(
                        "Ошибка",
                        f"Не удалось сохранить фото: {str(e)}"
                        )

    @classmethod
    def update_size(cls):
        """Изменяет размер изображения"""
        try:
            resized_image = cls.image.resize(
                (cls.width_val, cls.height_val),
                Image.LANCZOS
                )

            cls.image = resized_image

            max_size = (750, 500)
            display_image = resized_image.copy()
            if ((display_image.width > max_size[0]) or
                    (display_image.height > max_size[1])):
                display_image.thumbnail(max_size, Image.LANCZOS)

            new_photo = ImageTk.PhotoImage(display_image)
            cls.img_label.config(image=new_photo)
            cls.img_label.image = new_photo

            messagebox.showinfo("Успех", "Внесены изменения")
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось сохранить фото: {str(e)}"
                )

    @classmethod
    def change_size_window(cls):
        """Окно для изменения размера"""
        def apply_changes():
            """Функция - валидатор"""
            try:
                width_val = int(width.get())
                height_val = int(height.get())

                if width_val > 0 and height_val > 0:
                    dialog.destroy()
                    cls.width_val = width_val
                    cls.height_val = height_val
                    cls.update_size()
                else:
                    raise ValueError(
                        "Размеры должны быть положительными числами"
                        )
            except ValueError as e:
                messagebox.showerror("Ошибка", f"{str(e)}")

        dialog = Toplevel(cls.root)
        dialog.title("Изменить размер")

        Label(dialog, text="Ширина").grid(row=0, column=0, padx=5, pady=5)
        width = Entry(dialog)
        width.grid(row=0, column=1, padx=5, pady=5)

        Label(dialog, text="Высота").grid(row=1, column=0, padx=5, pady=5)
        height = Entry(dialog)
        height.grid(row=1, column=1, padx=5, pady=5)

        Button(
            dialog,
            text="Применить",
            command=lambda: apply_changes()
            ).grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        dialog.geometry("+300+300")
        dialog.transient(cls.root)
        dialog.grab_set()
        dialog.wait_window()

    @classmethod
    def bright_window(cls):
        """Окно для изменения яркости"""
        def apply_color():
            """Функция - валидатор"""
            try:
                b_val = int(down_blue.get())
                g_val = int(down_green.get())
                r_val = int(down_red.get())

                if all(0 <= val <= 255 for val in [b_val, g_val, r_val]):
                    cls.b_color_user = b_val
                    cls.g_color_user = g_val
                    cls.r_color_user = r_val
                    dialog_window.destroy()
                    cls.bright_color()
                else:
                    raise ValueError(
                        "Значения должны быть числами от 0 до 255"
                        )
            except ValueError as e:
                messagebox.showerror("Ошибка", f"{str(e)}")

        dialog_window = Toplevel(cls.root)
        dialog_window.title("Изменить яркость")

        Label(
            dialog_window,
            text=f"Введите значение для уменьшения синего спектра:"
            ).grid(row=0, column=0, padx=5, pady=5)
        down_blue = Entry(dialog_window)
        down_blue.grid(row=0, column=1, padx=5, pady=5)

        Label(
            dialog_window,
            text=f"Введите значение для уменьшения зеленого спектра:"
            ).grid(row=1, column=0, padx=5, pady=5)
        down_green = Entry(dialog_window)
        down_green.grid(row=1, column=1, padx=5, pady=5)

        Label(
            dialog_window,
            text=f"Введите значение для уменьшения красного спектра:"
            ).grid(row=2, column=0, padx=5, pady=5)
        down_red = Entry(dialog_window)
        down_red.grid(row=2, column=1, padx=5, pady=5)

        Button(
            dialog_window,
            text="Применить",
            command=apply_color
            ).grid(row=3, columnspan=2, column=0, pady=5, padx=5)

        dialog_window.resizable(False, False)
        dialog_window.geometry("+300+300")
        dialog_window.transient(cls.root)
        dialog_window.grab_set()
        dialog_window.wait_window()

    @classmethod
    def bright_color(cls):
        """Изменяет цвет изображения"""
        try:
            openсv_image = np.array(cls.image)

            openсv_image = cv2.cvtColor(openсv_image, cv2.COLOR_RGB2BGR)

            blue, green, red = cv2.split(openсv_image)

            blue = np.clip(
                blue.astype("int16") - cls.b_color_user, 0, 255
                ).astype("uint8")
            green = np.clip(
                green.astype("int16") - cls.g_color_user, 0, 255
                ).astype("uint8")
            red = np.clip(
                red.astype("int16") - cls.r_color_user, 0, 255
                ).astype("uint8")

            ready_image = cv2.merge((blue, green, red))

            ready_image_rgb = cv2.cvtColor(ready_image, cv2.COLOR_BGR2RGB)
            pil_ready_image = Image.fromarray(ready_image_rgb)
            cls.image = pil_ready_image

            display_image = cls.image.copy()
            max_size = (750, 500)
            if ((display_image.width > max_size[0]) or
                    (display_image.height > max_size[1])):
                display_image.thumbnail(max_size, Image.LANCZOS)

            ready_photo = ImageTk.PhotoImage(image=display_image)
            cls.img_label.config(image=ready_photo)
            cls.img_label.image = ready_photo

            messagebox.showinfo("Успех", "Внесены изменения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"{str(e)}")
            print(str(e))

    @classmethod
    def draw_circle_window(cls):
        """Открывает окно для рисования круга"""
        def apply_circle():
            """Функция - валидатор"""
            try:
                x_coord_val = int(x_coord.get())
                y_coord_val = int(y_coord.get())
                radius_val = int(radius.get())

                if ((0 <= x_coord_val <= cls.image.width) and
                        (0 <= y_coord_val <= cls.image.height)):
                    if radius_val >= 1:
                        cls.x_coord = x_coord_val
                        cls.y_coord = y_coord_val
                        cls.radius = radius_val
                        draw_dialog.destroy()
                        cls.draw_circle()
                    else:
                        raise ValueError(f"Радиус выходит за пределы значений")
                else:
                    raise ValueError(
                        f"Координаты вышли за пределы изображения"
                        )
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

        draw_dialog = Toplevel(cls.root)
        draw_dialog.title("Нарисовать круг")

        Label(
            draw_dialog,
            text="Координата x"
            ).grid(row=0, column=0, padx=5, pady=5)
        x_coord = Entry(draw_dialog)
        x_coord.grid(row=0, column=1, padx=5, pady=5)

        Label(draw_dialog, text="Координата y").grid(row=1, column=0, padx=5)
        y_coord = Entry(draw_dialog)
        y_coord.grid(row=1, column=1, padx=5, pady=5)

        Label(draw_dialog, text="Радиус").grid(row=2, column=0, padx=5, pady=5)
        radius = Entry(draw_dialog)
        radius.grid(row=2, column=1, padx=5, pady=5)

        Button(
            draw_dialog,
            text="Нарисовать",
            command=apply_circle
            ).grid(row=3, columnspan=2, column=0, pady=5, padx=5)

        draw_dialog.resizable(False, False)
        draw_dialog.geometry("+300+300")
        draw_dialog.transient(cls.root)
        draw_dialog.grab_set()
        draw_dialog.wait_window()

    @classmethod
    def draw_circle(cls):
        """Рисует круг на изображении"""
        openсv_image_draw = np.array(cls.image)
        openсv_image_draw = cv2.cvtColor(openсv_image_draw, cv2.COLOR_BGR2RGB)
        cv2.circle(
            openсv_image_draw,
            (cls.x_coord, cls.y_coord),
            cls.radius,
            (0, 0, 255),
            -1
            )

        openсv_image_draw = cv2.cvtColor(openсv_image_draw, cv2.COLOR_RGB2BGR)
        cls.image = Image.fromarray(openсv_image_draw)

        display_image = cls.image.copy()
        max_size = (750, 500)
        if ((display_image.width > max_size[0]) or
                (display_image.height > max_size[1])):
            display_image.thumbnail(max_size, Image.LANCZOS)

        ready_photo = ImageTk.PhotoImage(image=display_image)
        cls.img_label.config(image=ready_photo)
        cls.img_label.image = ready_photo

    @classmethod
    def save_image(cls):
        """Сохраняет изображение"""
        datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(
            str(Path.home() / "Downloads"),
            f"output_photo{datetime_str}.png"
            )
        messagebox.showinfo("Успех", f"Фото сохранено: {image_path}")
        cls.image.save(image_path)


App.create()
