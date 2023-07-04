import sys
sys.path.append(".")
from controller.controlador_enfermeiros import ControladorEnfermeiros
from view.tela_enfermeiro import TelaEnfermeiros
from controller.controlador_pacientes import ControladorPacientes
from view.tela_paciente import TelaPaciente
from controller.controlador_vacinas import ControladorVacina
from view.tela_vacina import TelaVacina
from controller.controlador_agendamentos import ControladorAgendamento
from view.tela_agendamento import TelaAgendamento
from view.tela_sistema import TelaSistema
from controller.excecoes import ListaVaziaException

from model.mediador import Mediator

class ControladorSistema():
    def __init__(self,  tela_sistema: TelaSistema, controlador_pacientes:ControladorPacientes, controlador_enfermeiros: ControladorEnfermeiros, controlador_vacinas: ControladorVacina, controlador_agendamento: ControladorAgendamento):
        self.__tela_sistema = tela_sistema
        self.__controlador_pacientes = controlador_pacientes
        self.__controlador_enfermeiros = controlador_enfermeiros
        self.__controlador_vacinas = controlador_vacinas
        self.__controlador_agendamento = controlador_agendamento
        self.__mediator = Mediator()
        # ^- ControladorAgendamento(TelaAgendamento(), self.__controlador_pacientes, self.__controlador_enfermeiros, self.__controlador_vacinas)
    
    def abre_menu_principal(self):

        lista_opcoes = {1: self.__controlador_enfermeiros.abre_tela_enfermeiros, 2: self.__controlador_pacientes.abre_tela_pacientes, 3: self.__controlador_agendamento.inicia_tela_agendamento, 4: self.__controlador_vacinas.inicia_tela_vacina, 5: self.listar_atendimentos_enfermeiro, 6: self.gera_relatorio}
        while True:
                valor_lido = self.__tela_sistema.mostra_menu_principal()
                if valor_lido == 0 or valor_lido == None:
                    exit()
                else:
                    lista_opcoes[valor_lido]()
             
    def listar_atendimentos_enfermeiro(self):
        while True:
            codigo_enfermeiro = self.__controlador_enfermeiros.seleciona_enfermeiro()
            if codigo_enfermeiro is None:
                break
            else:
                atendimentos_enfermeiro = []
                for agendamento in self.__controlador_agendamento.lista_agendamentos_concluidos():
                    if int(agendamento["codigo_enfermeiro"]) == codigo_enfermeiro:
                        atendimentos_enfermeiro.append(agendamento)
            try:
                if len(atendimentos_enfermeiro)>0:
                    self.__controlador_agendamento.mostra_atendimentos_enfermeiro(atendimentos_enfermeiro)
                    break
                else:
                    raise ListaVaziaException("atendimento para o enfermeiro selecionado")
            except ListaVaziaException as mensagem:
                self.__mediator.mensagem(mensagem)
            
    def gera_relatorio(self):
        lista_pacientes = self.__controlador_pacientes.lista_pacientes()
        if lista_pacientes is not None:
            total_doses_aplicadas = 0
            pacientes_fila = 0
            pacientes_primeira_dose = 0
            pacientes_segunda_dose = 0
            for paciente in lista_pacientes:
                if paciente['numero_doses'] == 0:
                    pacientes_fila +=1
                elif paciente['numero_doses'] == 1:
                    pacientes_primeira_dose += 1
                    total_doses_aplicadas += 1
                else:
                    pacientes_segunda_dose +=1
                    total_doses_aplicadas +=2
            self.__tela_sistema.mostra_relatorio({"fila": pacientes_fila, "total_primeira_dose": pacientes_primeira_dose, "total_segunda_dose": pacientes_segunda_dose, "total_doses": total_doses_aplicadas})
    

     

