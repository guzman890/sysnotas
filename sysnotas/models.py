# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from re import compile


class Alumno(models.Model):
    _name = 'sysnotas.alumno'
    _rec_name = "cui"

    cui = fields.Integer(string="CUI",
                         required=True,
                         index=True)

    nombre = fields.Char(string="Nombre",
                         size=30,
                         required=True)

    apellido = fields.Char(string="Apellidos",
                           size=30,
                           required=True)

    observacion = fields.Text(string="Observación",
                              help="Observaciones al alumno ")

    foto = fields.Binary(string="Foto")

    _sql_constraints = [
        ('alum_cui_uniq',
         'UNIQUE (alum_cui)',
         'El CUI no puede repetirse!')]

    @api.one
    @api.constrains('nombre')
    def check_value_re(self):
        pattern = compile("^[a-zA-Z]+$")
        if not pattern.match(self.nombre):
            msg = 'El campo Nombre sólo puede tener letras!'
            raise ValidationError(msg)

    @api.one
    @api.constrains('cui')
    def alum_cui_check(self):
        pattern = compile("^[1-9]{8}$")
        if not pattern.match(str(self.cui)):
            msg = "El campo CUI debe tener 8 números !"
            raise ValidationError(msg)


class curso(models.Model):
    _name = 'sysnotas.curso'
    _rec_name = "curs_nomb"

    curs_cod = fields.Integer(string = "Codigo", 
        required = True,
        index = True
        )
    curs_nomb = fields.Char( string = "Nombre", 
        size = 30,
        required = True
        )
    curs_cred = fields.Integer(string = "creditos",
        help = "cantidad de creditos "
        )
    curs_comp = fields.Text(string="Relacion de Horas",
        compute = "_show"
        )

    """ relaciones """
    curs_matr_cod = fields.Many2many(
        'sysnotas.matricula',
        string = 'matr_cod' 
        )
    curs_curs_hrio = fields.One2many(
        'sysnotas.crsho',
        'curs_curs_hrio',
        string = 'Relacion de horas'
        )
    _sql_constraints = [
        ('curs_cod_unique',
         'UNIQUE (curs_cod)',
         'El codigo de curso no puede repetirse!')]
    
    @api.one
    @api.depends('curs_curs_hrio')
    def _show(self):        
        self.curs_comp = " "
        _curso = self.curs_curs_hrio
        for c in range(0,len(_curso)):
            self.curs_comp+=str(_curso[c].crsho_tiph_cod.tiph_deno)+"-"+str(_curso[c].crsho_hrio_cod.hrio_deno)+" "
            

class matricula(models.Model):
    _name = 'sysnotas.matricula'
    _rec_name = "matr_cod"

    matr_cod = fields.Integer(string = "Codigo",
        help = "codigo de matricula",
        index = True
        )
    matr_nomb = fields.Char(string = "Codigo",
        help = "nombre de matricula",
        size = 30
        )
    matr_alum_mst = fields.Text(string = "Nombre", 
        store = False,
        compute = 'make_nombre'
        )

    """" relaciones """
    matr_alum_cui = fields.Many2one(
        'sysnotas.alumno',
        string = 'Cui de Alumno',
        index = True
        )

    matr_curs_cod = fields.Many2many(
        'sysnotas.curso',
        string = 'Cursos'
        )
    
    """ sql constraints"""
    _sql_constraints = [
        ('matr_cod_unique',
         'UNIQUE (matr_cod)',
         'El codigo de matricula no puede repetirse!')]

    #sql_constraints = [
    #    ('matr_alum_cui_2',
    #     'UNIQUE (matr_alum_cui)',
    #     'El codigo de alumno no puede repetirse!')]

    @api.one
    @api.depends('matr_alum_cui')
    def make_nombre(self):        
        if self.matr_alum_cui:
            self.matr_alum_mst = self.matr_alum_cui.alum_nomb +" "+ self.matr_alum_cui.alum_apel 


class Horario(models.Model):
    _name = 'sysnotas.horario'
    _rec_name = "hora"

    hora = fields.Integer(string="Hora",
                          required=True,
                          index=True,
                          help="Ejemplo: 13, 14, 7")

    _sql_constraints = [
        ('hrio_deno_unique',
         'UNIQUE (hora)',
         'Ya existe hora!')]


class TipoHorario(models.Model):
    _name = 'sysnotas.tipohorario'
    _rec_name = 'denominacion'

    denominacion = fields.Char(string="Siglas",
                               required=True,
                               size=2,
                               index=True,
                               help="Ejemplo: TE, LB, TP ")

    _sql_constraints = [
        ('tiph_deno_unique',
         'UNIQUE (denominacion)',
         'Ya existe tipo!')]

class curs_hrio(models.Model):
    _name = 'sysnotas.crsho'

    crsho_tiph_cod = fields.Many2one(
        'sysnotas.tiph',
        string = 'Tipo'
        )
    crsho_hrio_cod = fields.Many2one(
        'sysnotas.hrio',
        string = 'Horas'
        )

    curs_curs_hrio = fields.Many2one(
        'sysnotas.curso',
        string="relacion curso hora"
        )
