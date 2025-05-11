const getUfSigla = (uf: string): string => {
	switch (uf) {
		case 'Acre':
			return 'AC';
		case 'Alagoas':
			return 'AL';
		case 'Amapa':
			return 'AP';
		case 'Amazonas':
			return 'AM';
		case 'Bahia':
			return 'BA';
		case 'Ceara':
			return 'CE';
		case 'Distrito Federal':
			return 'DF';
		case 'Espirito Santo':
			return 'ES';
		case 'Goias':
			return 'GO';
		case 'Maranhao':
			return 'MA';
		case 'Mato Grosso':
			return 'MT';
		case 'Mato Grosso do Sul':
			return 'MS';
		case 'Minas Gerais':
			return 'MG';
		case 'Para':
			return 'PA';
		case 'Paraíba':
			return 'PB';
		case 'Parana':
			return 'PR';
		case 'Pernambuco':
			return 'PE';
		case 'Piaui':
			return 'PI';
		case 'Rio de Janeiro':
			return 'RJ';
		case 'Rio Grande do Norte':
			return 'RN';
		case 'Rio Grande do Sul':
			return 'RS';
		case 'Rondonia':
			return 'RO';
		case 'Roraima':
			return 'RR';
		case 'Santa Catarina':
			return 'SC';
		case 'Sao Paulo':
			return 'SP';
		case 'Sergipe':
			return 'SE';
		case 'Tocantins':
			return 'TO';
		default:
			return '';
	}
};

const getMunicipioCorrigido = (municipio: string): string => {
	switch (municipio) {
		case 'Chapeco':
			return 'Chapecó';
		case 'Sao Paulo':
			return 'São Paulo';
		default:
			return municipio;
	}
};

export { getUfSigla, getMunicipioCorrigido };
