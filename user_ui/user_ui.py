import gradio as gr
import requests_unixsocket

# Définir l'URL du socket Unix
SEND_URL = "http+unix://%2Ftmp%2Fapi_socket.sock/users/send"

def add_user(name):
    session = requests_unixsocket.Session()
    
    try:
        response = session.post(SEND_URL, params={"name": name})  # Passer `name` dans l'URL
        
        if response.status_code == 200:
            return response.json().get("message", "Utilisateur ajouté avec succès")
        else:
            return f"Erreur {response.status_code}: {response.text}"
    
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"
    
with gr.Blocks() as user_ui:
    gr.Markdown("# Interface Utilisateur 🧑‍💻")
    
    # Champ pour entrer le nom
    name_input = gr.Textbox(label="Entrez votre nom")
    
    # Bouton d'envoi
    submit_button = gr.Button("Envoyer")
    
    # Zone de texte pour afficher le résultat
    output_message = gr.Textbox(label="Résultat", interactive=False)

    # Lier le bouton à la fonction
    submit_button.click(fn=add_user, inputs=name_input, outputs=output_message)

# Lancer l'interface Gradio
user_ui.launch(server_name="0.0.0.0", server_port=7860, share=True)
