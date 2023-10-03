from pprint import pprint
import time
from kucoin.client import Market
from kucoin.client import Trade, User
from kucoin.market import market
from flask import Flask, render_template, request, redirect, url_for,jsonify
import threading

app = Flask(__name__)

# market = market.MarketData(url='https://api.kucoin.com')


api_passphrase = 'trastoshen'
api_key = '6517f87b7962f9000162b1b1'
api_secret = 'b7f1a87f-7237-4b83-aa07-3efa4b0addb0'
client = Trade(api_key,api_secret,api_passphrase)
clientMerkat = Market(api_key,api_secret,api_passphrase)
user = User(api_key,api_secret,api_passphrase)


saldoUSDThtml = 0

repetir = True
precioParaVentaLink = 8.2

precioParaCompraLink = 5.7
precioParaCompraSol = 9.6
precioParaComprakcs = 2.7
precioParaCompraySQUAD = 0.0016

compramosLink = False
compramosSOL = False
compramosKCS = False
compramosSQUAD = False

precioDeCompraLink = 0
precioDeCompraSOL = 0
precioDeCompraYFDAI = 0
precioDeCompraKCS = 0

saldoLINK = 0
saldoSQUAD =  0
saldoUSDT = 0
saldoKCS = 0
saldoSOL = 0

caidaDeOtrasMonedas = False
caidaDeSol = False
caidaDeKcs = False
caidaDeSQUAD = False

mensajeERROR = "Sin errores"
mensajeACTIVIDAD = "Sin actividad"
vueltas = 0
precioSQUAD = 0
precioLINK = 0
precioSOL = 0
def actualizar_datos():
    

    global precioSOL,precioLINK,precioSQUAD, vueltas, saldoSOL, saldoUSDT , saldoKCS, saldoSQUAD, saldoLINK, mensajeERROR, mensajeACTIVIDAD
    mensajeACTIVIDAD = "Sin actividad"+str(vueltas)
    
    vueltas = vueltas +1

 
    try :

      balances = user.get_account_list()
      
      for balance in balances:
          if (balance['currency']  == "LINK") and ( balance['type'] == "trade" ) :
              saldoLINK = round(float(balance['balance']),2)
              
          if ((balance['currency'])  == "SQUAD")  and ( balance['type'] == "trade" ) :
              saldoSQUAD = round(float(balance['balance']),2)
              
          if ((balance['currency'])  == "USDT")  and ( balance['type'] == "trade" ) :
              saldoUSDT =round(float(balance['balance']),2)
             
              
          if ((balance['currency'])  == "KCS")  and ( balance['type'] == "trade" ) :
              saldoKCS = round(float(balance['balance']),2)
            
          if ((balance['currency'])  == "SOL")  and ( balance['type'] == "trade" ) :
              saldoSOL = round(float(balance['balance']),2)
            
      print("saldo "+str(saldoUSDT))
      precioSOL = float(clientMerkat.get_24h_stats("SOL-USDT")["buy"])
      precioLINK =   float(clientMerkat.get_24h_stats("LINK-USDT")["buy"])
      precioKCS = float(clientMerkat.get_24h_stats("KCS-USDT")["buy"])
      precioSQUAD = float(clientMerkat.get_24h_stats("SQUAD-USDT")["buy"])
      
     


      # pprint("saldo usdt :"+(str(saldoUSDT)))
      # print("Precio link: "+str(precioLINK))
      # print("Precio sol: "+str(precioSol))
      # print("Precio kcs: "+str(precioKCS))
      # print("Precio SQUAD: "+str(precioSQUAD))

      caidaDeSol = True if precioSOL <= precioParaCompraSol else False
      caidaDekcs = True if precioKCS <= precioParaComprakcs else False
      caidaDeSQUAD = True if precioSQUAD <= precioParaCompraySQUAD else False

      caidaDeOtrasMonedas = True if( (caidaDeKcs) or (caidaDeSol) or (caidaDeSQUAD) )else  False

      

      if not caidaDeOtrasMonedas :
          
        if ((precioLINK > precioParaVentaLink )) and not ( compramosLink ) :
          mensajeACTIVIDAD = "Hemos vendido link a :"+str(precioLINK)
          cantidadVenta =  round((saldoLINK * precioLINK),2)
          ventaLink = client.create_market_order(symbol="LINK-USDT",side="sell",type="market", size=None, funds=cantidadVenta, client_oid=None, remark=None, stp=None)
          compramosLink = False
        


        if ((precioLINK < precioParaCompraLink) ) and (not compramosLink)  : 
          mensajeACTIVIDAD = "Hemos comprado link a :"+str(precioLINK)
          cantidadCompraLink = round(saldoUSDT,2)  
          precioDeCompraLink = precioLINK
          compraLink = client.create_market_order(symbol="LINK-USDT",side="buy",type="market", size=None, funds=cantidadCompraLink, client_oid=None, remark=None, stp=None)
          compramosLink = True
        
      else : 

        if saldoLINK > 1 :
          
          cantidadVenta =  round((saldoLINK * precioLINK),2)
          ventaLink = client.create_market_order(symbol="LINK-USDT",side="sell",type="market", size=None, funds=cantidadVenta, client_oid=None, remark=None, stp=None)
        
        if caidaDeSol and not compramosSOL:
          cantidadCompraSOL =  round(saldoUSDT-1,2) 
          mensajeACTIVIDAD = ("ha caido sol y compramos sol "+str(cantidadCompraSOL))
          precioDeCompraSOL = precioSOL
          compraSOL = client.create_market_order(symbol="SOL-USDT",side="buy",type="market", size=None, funds=cantidadCompraSOL, client_oid=None, remark=None, stp=None)
          compramosSOL = True
        else : 
            print("ya hemos comprado")

        if caidaDeKcs and not compramosKCS: 
          cantidadCompraKCS =  round(saldoUSDT,2) 
          mensajeACTIVIDAD = ("ha caido kcs y compramos sol "+str(cantidadCompraSOL))

          precioDeCompraKCS = precioKCS
          compraKCS = client.create_market_order(symbol="KCS-USDT",side="buy",type="market", size=None, funds=cantidadCompraKCS, client_oid=None, remark=None, stp=None)
          compramosKCS = True
            
        if caidaDeSQUAD and not compramosSQUAD: 
          cantidadCompraSQUAD =  round(saldoUSDT,2)  
          precioDeCompraSQUAD = precioSQUAD
          mensajeACTIVIDAD = ("ha caido SQUAD y compramos sol "+str(cantidadCompraSOL))
          compraSQUAD = client.create_market_order(symbol="SQUAD-USDT",side="buy",type="market", size=None, funds=cantidadCompraSQUAD, client_oid=None, remark=None, stp=None)
          compramosSQUAD = True

    except Exception as e:

      mensajeERROR = ("Algun error con la api"+str(e))
    


# Esta función se ejecutará en un hilo para actualizar los datos periódicamente
def actualizar_periodicamente():
    while True:
        actualizar_datos()
        
        # Espera 5 segundos antes de actualizar nuevamente
        threading.Event().wait(2)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Verifica las credenciales (esto debe reemplazarse en una aplicación real)
    if email == 'cristian' and password == '1':
        # Inicia el hilo para actualizar los datos periódicamente
        t = threading.Thread(target=actualizar_periodicamente)
        t.daemon = True
        t.start()
     
        return redirect('/dashboard')
    else:
        return "Credenciales incorrectas"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',precioSOL = precioSOL,precioSQUAD = precioSQUAD, precioLINK = precioLINK,saldoSOL = saldoSOL ,saldoLINK = saldoLINK,  saldoUSDT= saldoUSDT, saldoKCSHTML= saldoKCS, saldoSQUAD= saldoSQUAD, mensajeERROR= mensajeERROR, mensajeACTIVIDAD=mensajeACTIVIDAD)

if __name__ == '__main__':
    app.run(debug=True)