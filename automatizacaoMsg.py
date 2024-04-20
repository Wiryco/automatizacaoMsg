import scripts
import functions

if __name__ == '__main__':
    functions.openWppDektop()
    
    dba = functions.dataBase()
    query = scripts.querys()

    for contato in dba.select(query=query.consultaDadosCliente()).itertuples():
        contato_wpp = functions.contatoWpp(dadosContato=contato)

        contato_wpp.eventSelectUser()

        if contato.ID_TIPO_ENVIO == 1 and contato.DESCRICAO_MENSAGEM:
            contato_wpp.eventSendMsg()

        if (contato.ID_TIPO_ENVIO == 2 or contato.ID_TIPO_ENVIO == 3) and contato.CAMINHO_ARQUIVO:
            contato_wpp.eventClickFile()
            contato_wpp.eventSendFile()