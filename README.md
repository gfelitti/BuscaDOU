## Guia de Uso do BuscaDOU

![Python 3.9](https://img.shields.io/badge/python-%3E%3D3.9-blue)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/15mF8bDk223k_Rn3o-eQMMMWEvNlGsgqC?usp=sharing#scrollTo=UhvOUzCUb8Jf)

Projeto organizado por [Heloísa Vasconcelos](https://www.linkedin.com/in/helo%C3%ADsa-vasconcelos-552a00108/), [Natália Santos](https://www.linkedin.com/in/nataliamfsantos/) e [Guilherme Felitti](https://www.linkedin.com/in/guilhermefelitti/).

Este guia fornece instruções detalhadas sobre como instalar as dependências necessárias e usar o script para raspar informações do Diário Oficial da União (DOU) com base em um termo de busca e uma data específica.

Não sabe usar o Terminal? Sem problema: [use o código no Colab](https://colab.research.google.com/drive/15mF8bDk223k_Rn3o-eQMMMWEvNlGsgqC?usp=sharing#scrollTo=UhvOUzCUb8Jf).
### Pré-requisitos

Antes de começar, certifique-se de que você tem o Python +3.9 instalado em seu sistema. Você também precisará de `pip` para instalar as bibliotecas necessárias.

### Configuração do Ambiente

1. **Clonar o Repositório ou Baixar o Script**

   Primeiro, obtenha o script de raspagem do DOU, clonando o repositório ou baixando o arquivo diretamente do local fornecido.

2. **Instalar Dependências**

   Navegue até o diretório do projeto e instale as dependências listadas no `requirements.txt`. Abra o terminal ou prompt de comando e execute o seguinte comando:

   ```bash
   pip install -r requirements.txt
   ```

   Isso instalará todas as bibliotecas necessárias, como `requests`, `pandas`, `beautifulsoup4`, e `tqdm`.

### Utilização do Script

O script é acionado via linha de comando. Aqui estão os detalhes sobre como executá-lo com os parâmetros necessários:

#### Parâmetros do Script

- `--termo` ou `-t`: O termo de busca para filtrar as publicações no DOU.
- `--data` ou `-d`: A data específica para a qual raspar as publicações. Formato da data deve ser `dd-mm-aaa`. Se não especificado, o script usará o dia de hoje.

#### Comandos para Executar o Script

Abra o terminal ou prompt de comando e navegue até o diretório onde o script está localizado. Execute o script com os parâmetros necessários, por exemplo:

```bash
python dou.py --termo licitação --data 21-05-2024
```

Se você quiser usar a data atual e apenas especificar um termo, você pode omitir o parâmetro `--data`:

```bash
python dou.py --termo contrato
```

### Resultados

Após a execução do script:

- Será gerado um arquivo `CSV` com todos os dados raspados antes da filtragem nomeado como `DOU_bruto_dd-mm-aaaa.csv`.
- Se houver resultados correspondentes ao termo, um segundo arquivo `CSV` será gerado, contendo apenas os registros filtrados, nomeado `DOU_filtrado_dd-mm-aaaa.csv`.
- Logs serão exibidos no terminal para informar sobre o processo de raspagem, avisos e erros.

### Problemas Comuns

- **Dependências não instaladas**: Certifique-se de que todos os pacotes listados no `requirements.txt` estão instalados corretamente.
- **Erros de script**: Verifique se o formato da data está correto e se o termo de busca não contém caracteres inválidos.
- **Não abuse do site da Imprensa Nacional**: O script raspa os cadernos do DOU completos. Só rode 1x por dia para não abusar os servidores da Imprensa Nacional. O script gera um arquivo bruto para permitir novas filtragens sem precisar fazer uma nova extração.
- **No fim do dia, site fica instável**: No fim do dia, o site da Imprensa Nacional costuma ficar instável. Prefira fazer a extração mais cedo ou mais tarde.
