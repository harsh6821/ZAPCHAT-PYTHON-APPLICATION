import flet as ft

# Message class with username, text, and message type
class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

# Custom ChatMessage class inheriting from Row
#class ChatMessage defines how a single chat message will be in a row
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START

        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    # Get the first letter of the user's name for the avatar
    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()
        #takes the first character of the user_name and ensures it is in uppercase

    # Get a color based on the hash of the user's name
    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
    #hash- for converting to integer value
    #%len- to generate a random colour

# Main application
def main(page: ft.Page):

    # Chat messages display area as a scrollable ListView with auto-scroll
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,  # Auto-scroll to the latest message
    )

    # New message input field with on_submit and Shift+Enter behavior
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,  # Focus on this field when the dialog closes
        shift_enter=True,  # Shift+Enter for multiline, Enter for submit
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=lambda e: send_message_click(None),  # Submit on Enter key
    )

    # Function to handle displaying chat messages
    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.GREEN, size=12)
        chat.controls.append(m)
        page.update()

    # Subscribe to pubsub for receiving messages
    page.pubsub.subscribe(on_message)

    # Join chat function
    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Name cannot be blank!"
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(
                Message(user_name=user_name.value, text=f"{user_name.value} has joined the chat.", message_type="login_message")
            )
            page.update()

    # Send message function
    def send_message_click(e):
        page.pubsub.send_all(
            Message(user_name=page.session.get('user_name'), text=new_message.value, message_type="chat_message")
        )
        new_message.value = ""
        new_message.focus()  # Refocus the input field after submitting
        page.update()

    # User name dialog at startup with autofocus
    user_name = ft.TextField(label="Enter your name", autofocus=True)
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_click)],
        actions_alignment="end",
    )

    # Add everything to the page, including chat and input controls
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

ft.app(main)
