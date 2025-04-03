import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import ssl

# Configuração do logger
logger = logging.getLogger(__name__)
load_dotenv()

async def send_email(to_email: str, subject: str, body: str, filename: str = None):
    try:
        logger.info(f"Iniciando envio de e-mail para: {to_email}")
        
        # Validação robusta do e-mail (nova implementação)
        if not to_email or not isinstance(to_email, str):
            logger.error("E-mail não pode ser vazio ou não é string")
            raise ValueError("E-mail do destinatário não pode ser vazio")
            
        if "@" not in to_email or "." not in to_email.split("@")[-1]:
            logger.error(f"Formato de e-mail inválido: {to_email}")
            raise ValueError("Formato de e-mail inválido. Use user@domain.com")

        # Configuração da mensagem
        msg = MIMEMultipart()
        msg['From'] = os.getenv("SMTP_USER")
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Anexo do PDF (com verificação de arquivo)
        if filename:
            if not os.path.exists(filename):
                logger.error(f"Arquivo não encontrado: {filename}")
                raise FileNotFoundError(f"Arquivo {filename} não existe")
                
            logger.info(f"Preparando anexo: {filename}")
            with open(filename, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(filename)}"'
            )
            msg.attach(part)

        # Conexão SMTP segura com timeout
        context = ssl.create_default_context()
        
        with smtplib.SMTP(
            host=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT")),
            timeout=10  # Timeout de 10 segundos
        ) as server:
            server.set_debuglevel(0)  # Log detalhado SMTP
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            
            # Valida credenciais antes do login
            if not all([os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD")]):
                raise ValueError("Credenciais SMTP não configuradas no .env")
                
            server.login(
                user=os.getenv("SMTP_USER"),
                password=os.getenv("SMTP_PASSWORD")
            )
            
            # Envio com tratamento explícito
            server.sendmail(
                from_addr=os.getenv("SMTP_USER"),
                to_addrs=to_email,
                msg=msg.as_string()
            )
        
        logger.info(f"E-mail enviado com sucesso para {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error("Falha na autenticação SMTP", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail="Falha na autenticação no servidor de e-mail"
        )
    except smtplib.SMTPException as e:
        logger.error(f"Erro SMTP: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail=f"Erro no servidor SMTP: {e.smtp_error.decode() if hasattr(e, 'smtp_error') else str(e)}"
        )
    except Exception as e:
        logger.error(f"Erro inesperado: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar e-mail: {str(e)}"
        )