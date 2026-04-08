import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send_order_confirmation(self, customer_email, order_details, gst_rate, shipping_info, refund_policy):
        # Calculate GST
        order_total = order_details['total']
        gst_amount = order_total * gst_rate / 100
        total_amount = order_total + gst_amount

        # Create the email content
        subject = "Order Confirmation"
        body = f"""
        Dear Customer,

        Thank you for your order. Here are your order details:

        Order ID: {order_details['order_id']}
        Order Total: {order_total:.2f}
        GST ({gst_rate}%): {gst_amount:.2f}
        Total Amount: {total_amount:.2f}

        Shipping Information:
        {shipping_info}

        Refund Policy:
        {refund_policy}

        Thank you for shopping with us!

        Regards,
        Your Company Name
        """

        # Prepare the email
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = customer_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Enable security
                server.login(self.username, self.password)
                server.send_message(msg)
                print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    email_service = EmailService('smtp.example.com', 587, 'your_email@example.com', 'your_password')
    order_details = {'order_id': '123456', 'total': 100.0}
    gst_rate = 18  # Example GST rate
    shipping_info = "123 Shipping Lane, Ship City, SH"
    refund_policy = "You can request a refund within 30 days of purchase."
    
    email_service.send_order_confirmation('customer@example.com', order_details, gst_rate, shipping_info, refund_policy)