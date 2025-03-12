import gradio as gr
import requests_unixsocket

# Définir l'URL du socket Unix
GET_USERS_URL = "http+unix://%2Ftmp%2Fapi_socket.sock/admin/users"
DELETE_USER_URL = "http+unix://%2Ftmp%2Fapi_socket.sock/admin/users/delete"

def get_users():
    session = requests_unixsocket.Session()  # Créer une session pour utiliser le socket Unix
    response = session.get(GET_USERS_URL)
    return "\n".join([f"{user['id']}: {user['name']}" for user in response.json()])

def delete_user(user_id):
    session = requests_unixsocket.Session()  # Créer une session pour utiliser le socket Unix
    response = session.delete(DELETE_USER_URL, params={"user_id": int(user_id)})
    return response.json()["message"]

with gr.Blocks() as admin_ui:
    gr.Markdown("# Interface Admin 👑")

    with gr.Row():
        get_users_button = gr.Button("Afficher les utilisateurs")
        users_list = gr.Textbox(label="Liste des utilisateurs", interactive=False)
        get_users_button.click(fn=get_users, inputs=[], outputs=users_list)

    with gr.Row():
        user_id_input = gr.Textbox(label="ID de l'utilisateur à supprimer")
        delete_button = gr.Button("Supprimer")
        delete_result = gr.Textbox(label="Résultat")
        delete_button.click(fn=delete_user, inputs=user_id_input, outputs=delete_result)

admin_ui.launch(server_name="0.0.0.0", server_port=7861, share=True)
