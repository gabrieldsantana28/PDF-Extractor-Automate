from dataclasses import dataclass


@dataclass
class Unimed:

    def __init__(
            self,
            ds_nome_unimed,
            cd_unimed,
            cd_ans,
            ds_municipio,
            ds_estado,
            ds_regiao,
            ds_tipo_cooperativa
    ):
        self.ds_nome_unimed = ds_nome_unimed
        self.cd_unimed = cd_unimed
        self.cd_ans = cd_ans
        self.ds_municipio = ds_municipio
        self.ds_estado = ds_estado
        self.ds_regiao = ds_regiao
        self.ds_tipo_cooperativa = ds_tipo_cooperativa