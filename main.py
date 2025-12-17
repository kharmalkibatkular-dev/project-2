from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.graphics.texture import Texture

# -----------------------------
# GLOBAL STORAGE
# -----------------------------
orders = []
order_id = 1

# -----------------------------
# CUSTOM CARD WIDGET
# -----------------------------
class Card(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.padding = 12
        self.spacing = 10
        self.size_hint_y = None
        self.height = 65
        self.orientation = "horizontal"

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(radius=[15])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# -----------------------------
# PRETTY BUTTON
# -----------------------------
class PrettyButton(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.font_size = 20
        self.size_hint_y = None
        self.height = 55
        self.background_normal = ""
        self.background_color = (0.2, 0.5, 0.9, 1)
        self.color = (1, 1, 1, 1)


# -----------------------------
# BASE SCREEN WITH GRADIENT
# -----------------------------
class GradientScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create gradient texture
        texture = Texture.create(size=(1, 64), colorfmt='rgba')
        buf = []

        for i in range(64):
            r = int(51 + (204 - 51) * i / 63)
            g = int(153 + (230 - 153) * i / 63)
            b = int(230 + (255 - 230) * i / 63)
            a = 255
            buf.extend([r, g, b, a])

        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        texture.wrap = 'repeat'
        texture.uvsize = (1, -1)

        with self.canvas.before:
            self.bg_rect = Rectangle(texture=texture, pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# -----------------------------
# LOGIN SCREEN
# -----------------------------
class LoginScreen(GradientScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        # Logo
        logo = Image(source="laundry_logo.png", size_hint=(0.3, 0.3),
                     allow_stretch=True, keep_ratio=True)
        layout.add_widget(logo)

        # Title
        title = Label(text="[b]QuickWash Login[/b]", markup=True, font_size=38, color=(1, 1, 1, 1))
        layout.add_widget(title)

        # Card
        card = BoxLayout(orientation="vertical", padding=20, spacing=15,
                         size_hint=(0.85, None), height=350)

        with card.canvas.before:
            Color(1, 1, 1, 1)
            card.rect = RoundedRectangle(radius=[25])

        card.bind(pos=lambda inst, val: setattr(card.rect, 'pos', card.pos),
                  size=lambda inst, val: setattr(card.rect, 'size', card.size))

        self.username = TextInput(hint_text="Email", multiline=False)
        self.password = TextInput(hint_text="Password", password=True, multiline=False)

        login_btn = PrettyButton(text="Login")
        login_btn.bind(on_press=self.login)

        google_btn = PrettyButton(text="Login with Google", background_color=(0.85, 0.1, 0.1, 1))
        google_btn.bind(on_press=self.fake_google)

        create_btn = Button(
            text="[b]Create New Account[/b]", markup=True,
            background_normal="", background_color=(0, 0, 0, 0),
            color=(0.2, 0.5, 0.9, 1), size_hint_y=None, height=40, font_size=18
        )
        create_btn.bind(on_press=lambda x: setattr(self.manager, "current", "signup"))

        card.add_widget(self.username)
        card.add_widget(self.password)
        card.add_widget(login_btn)
        card.add_widget(google_btn)
        card.add_widget(create_btn)

        layout.add_widget(card)
        self.add_widget(layout)

    def login(self, *args):
        self.manager.current = "home"

    def fake_google(self, *args):
        self.manager.current = "home"


# -----------------------------
# SIGNUP SCREEN
# -----------------------------
class SignupScreen(GradientScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        title = Label(text="[b]Create Account[/b]", markup=True, font_size=34, color=(1, 1, 1, 1))

        card = BoxLayout(orientation="vertical", padding=20, spacing=15, size_hint=(0.85, None), height=350)

        with card.canvas.before:
            Color(1, 1, 1, 1)
            card.rect = RoundedRectangle(radius=[25])

        card.bind(pos=lambda instance, value: setattr(card.rect, 'pos', card.pos),
                  size=lambda instance, value: setattr(card.rect, 'size', card.size))

        self.email = TextInput(hint_text="Email", multiline=False)
        self.password = TextInput(hint_text="Password", password=True, multiline=False)
        self.confirm = TextInput(hint_text="Confirm Password", password=True, multiline=False)

        signup_btn = PrettyButton(text="Create Account")
        signup_btn.bind(on_press=self.create_account)

        back_btn = PrettyButton(text="Back to Login", background_color=(0.4, 0.4, 0.4, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "login"))

        card.add_widget(self.email)
        card.add_widget(self.password)
        card.add_widget(self.confirm)
        card.add_widget(signup_btn)
        card.add_widget(back_btn)

        layout.add_widget(title)
        layout.add_widget(card)
        self.add_widget(layout)

    def create_account(self, *args):
        self.manager.current = "login"


# -----------------------------
# HOME SCREEN
# -----------------------------
class HomeScreen(GradientScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=30)

        title = Label(text="[b]QuickWash Laundry[/b]",
                      markup=True, font_size=38,
                      color=(0, 0, 0, 1), size_hint=(1, 0.2))

        order_btn = PrettyButton(text="Place New Order")
        order_btn.bind(on_press=lambda x: setattr(self.manager, "current", "order"))

        list_btn = PrettyButton(text="Track / View Orders")
        list_btn.bind(on_press=lambda x: self.goto_list())

        layout.add_widget(title)
        layout.add_widget(order_btn)
        layout.add_widget(list_btn)

        self.add_widget(layout)

    def goto_list(self):
        self.manager.get_screen("list").load_orders()
        self.manager.current = "list"


# -----------------------------
# ORDER SCREEN
# -----------------------------
class OrderScreen(GradientScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        title = Label(text="[b]Place Laundry Order[/b]", markup=True, font_size=30, color=(0, 0, 0, 1))

        self.clothes = TextInput(hint_text="Clothes count", multiline=False)
        self.address = TextInput(hint_text="Pickup address")

        submit_btn = PrettyButton(text="Submit Order")
        submit_btn.bind(on_press=self.submit)

        back_btn = PrettyButton(text="Back")
        back_btn.background_color = (0.4, 0.4, 0.4, 1)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))

        layout.add_widget(title)
        layout.add_widget(self.clothes)
        layout.add_widget(self.address)
        layout.add_widget(submit_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def submit(self, *args):
        global order_id

        orders.append({
            "id": order_id,
            "clothes": self.clothes.text,
            "address": self.address.text,
            "status": "Pending"
        })

        order_id += 1
        self.clothes.text = ""
        self.address.text = ""

        self.manager.get_screen("list").load_orders()
        self.manager.current = "list"


# -----------------------------
# ORDER LIST SCREEN
# -----------------------------
class OrderListScreen(GradientScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        main = BoxLayout(orientation="vertical", padding=30, spacing=20)

        self.title = Label(text="[b]Order List[/b]",
                           markup=True, font_size=32,
                           color=(0, 0, 0, 1))

        main.add_widget(self.title)

        scroll = ScrollView(size_hint=(1, 0.8))
        self.box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=15)
        self.box.bind(minimum_height=self.box.setter("height"))
        scroll.add_widget(self.box)

        back_btn = PrettyButton(text="Back")
        back_btn.background_color = (0.4, 0.4, 0.4, 1)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))

        main.add_widget(scroll)
        main.add_widget(back_btn)

        self.add_widget(main)

    def load_orders(self):
        self.box.clear_widgets()

        for order in orders:
            card = Card()

            info = Label(
                text=f"[b]Order #{order['id']}[/b]\n{order['clothes']} clothes | {order['address']}",
                markup=True, size_hint_x=0.7, color=(0, 0, 0, 1)
            )

            status_btn = PrettyButton(text=order["status"], size_hint_x=0.3)
            status_btn.bind(on_press=lambda x, o=order: self.open_update(o))

            card.add_widget(info)
            card.add_widget(status_btn)
            self.box.add_widget(card)

    def open_update(self, order):
        screen = self.manager.get_screen("update")
        screen.load_order(order)
        self.manager.current = "update"


# -----------------------------
# UPDATE STATUS SCREEN
# -----------------------------
class UpdateOrderScreen(GradientScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.order = None

        layout = BoxLayout(orientation="vertical", padding=40, spacing=25)

        self.title = Label(text="", markup=True, font_size=28, color=(0, 0, 0, 1))
        layout.add_widget(self.title)

        pending = PrettyButton(text="Set: Pending")
        pending.bind(on_press=lambda x: self.update("Pending"))

        processing = PrettyButton(text="Set: Processing")
        processing.bind(on_press=lambda x: self.update("Processing"))

        completed = PrettyButton(text="Set: Completed")
        completed.bind(on_press=lambda x: self.update("Completed"))

        back = PrettyButton(text="Back")
        back.background_color = (0.4, 0.4, 0.4, 1)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "list"))

        layout.add_widget(pending)
        layout.add_widget(processing)
        layout.add_widget(completed)
        layout.add_widget(back)

        self.add_widget(layout)

    def load_order(self, order):
        self.order = order
        self.title.text = (
            f"[b]Order #{order['id']}[/b]\n"
            f"Clothes: {order['clothes']}\n"
            f"Address: {order['address']}\n"
            f"Status: {order['status']}"
        )

    def update(self, status):
        self.order["status"] = status
        self.manager.get_screen("list").load_orders()
        self.manager.current = "list"


# -----------------------------
# MAIN APP
# -----------------------------
class LaundryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(OrderScreen(name="order"))
        sm.add_widget(OrderListScreen(name="list"))
        sm.add_widget(UpdateOrderScreen(name="update"))
        return sm


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    LaundryApp().run()
