from fpdf import FPDF
from app.schemas.user import User

def generate_user_pdf(users: list[User], filename: str = "usuarios.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Relatório de Usuários", ln=1, align="C")
    pdf.ln(10)

    for user in users:
        pdf.cell(200, 10, txt=f"ID: {user.id}", ln=1)
        pdf.cell(200, 10, txt=f"Nome: {user.name}", ln=1)
        pdf.cell(200, 10, txt=f"E-mail: {user.email}", ln=1)
        pdf.ln(5)

    pdf.output(filename)
    return filename