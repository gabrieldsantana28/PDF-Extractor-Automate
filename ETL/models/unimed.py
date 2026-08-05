from dataclasses import dataclass


@dataclass
class Unimed:

    cd_unimed: int
    ds_unimed: str
    cd_ans: int
    ds_regiao: str
    ds_estado: str
    ds_municipio: str
    tp_cooperativa: str

    qtd_beneficiarios: int
    qtd_colaboradores: int
    qtd_medicos: int
    ds_porte: str