#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORTA 5000 // Porta para comunicar com o servidor
#define TAM 512    // Tamanho do buffer para envio de dados

int main ()
{
  int sockfd; // Descritor do socket que aguarda conexao
				    
  /* Obtem um descritor para o socket que aguarda conexão */
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
  {
     printf ("ERROR: Falha ao obter descritor do socket.\n");
     return 0;
  }else
     printf ("[servidor] Descritor do socket obtido com sucesso.\n");
  					    
  
  /* Preenche a estrutura de enderecamento do socket local */
  struct sockaddr_in addr_local;  // Enderecar o socket local
  addr_local.sin_family = AF_INET; // Protocolos da internet 
  addr_local.sin_port = htons(PORTA); // Numero da porta
  addr_local.sin_addr.s_addr = INADDR_ANY; // Qualquer IP
  bzero(&(addr_local.sin_zero), 8); // Zera o resto da estrutura
							    
  /* Associa o descritor do socket ao endereco definido */
  if(bind(sockfd, (struct sockaddr*)&addr_local, sizeof(struct sockaddr)) == -1)
  {
     printf ("ERROR: Falha ao associar descritor do socket a porta %d.\n",PORTA);
     return (0);
  } else
     printf("[servidor] Associou a porta %d no IP 0.0.0.0 com sucesso.\n",PORTA);
  
  /* Aguarda (e possivelmente enfileira) conexoes remotas */
  if(listen(sockfd,5) == -1)
  {
    printf ("ERROR: Ao ouvir porta %d.\n", PORTA);				
    return (0);
  }else
    printf ("[servidor] Ouvindo a porta %d com sucesso. \n", PORTA);
    
  unsigned int addr_size = sizeof(struct sockaddr_in); // tamanho da estrutura
  int novo_sockfd; // Descritor para o socket da nova conexao (que sera criada)
  struct sockaddr_in addr_remoto; // Usada para enderecar o socket remoto 
  
  while(1)
  {
      /* Aguarda conexao, e obtem um novo descritor de socket para a conexao */
      if((novo_sockfd = accept(sockfd,(struct sockaddr *)&addr_remoto, &addr_size)) == -1)
      {
         printf ("ERROR: Obtendo novo descritor de socket para a conexao.\n");	
      }else{ 
         printf ("[servidor] Obteve uma conexao com %s.\n", inet_ntoa(addr_remoto.sin_addr));	
         
	 char sdbuf[TAM]; // Buffer de envio
         sprintf(sdbuf,"Envie-me o nome do arquivo a ser transferido. \n");
         if(send(novo_sockfd, sdbuf, strlen(sdbuf)+1, 0) < 0)
	 {  
	    printf("ERROR: Falha ao enviar solicitacao de arquivo.\n");	    
	    close(novo_sockfd);
	 }else{  
	    printf("[servidor->cliente] %s \n", sdbuf);
	    printf("Aguardando resposta...\n");

	    char recvbuf[TAM]; // Buffer de recepcao
	    int f_name_sz;
	    if((f_name_sz = recv(novo_sockfd, recvbuf, TAM, 0))<=0)
	    {
	       printf("ERROR: Falha ao receber nome do arquivo.\n");
	       close(novo_sockfd);	    
	    }else{
	       printf("[servidor]: Nome do arquivo a ser trasnferido %s \n",recvbuf);
               printf("[servidor]: Abrindo arquivo...\n");
	       
               recvbuf[f_name_sz-2] = '\0';
	       FILE *fp = fopen(recvbuf,"r");
	       if(fp == NULL)
	       {
	         printf("ERROR: Arquivo %s nao encontrado.\n", recvbuf); 
	         close(novo_sockfd);
	       }else{	            
	          bzero(sdbuf, TAM); //Limpa o buffer de envio
	          printf("[servidor]: Transferindo o arquivo solicitado...\n");
	          int f_block_sz;
	          while((f_block_sz = fread(sdbuf, sizeof(char), TAM, fp))>0)
	          {   
	            if(send(novo_sockfd, sdbuf, f_block_sz, 0) < 0)
	            {
	              printf("ERROR: Falha ao enviar o arquivo %s.\n", recvbuf);
	              break;
	            }
	            bzero(sdbuf, TAM);
	          }
		  printf("ok! Arquivo transferido. \n");
	       }
	    }  
	 }
      }	    
      close(novo_sockfd);
      printf("Aguardando nova conexao... \n");
  }
}
