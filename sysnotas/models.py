# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
from openerp.exceptions import ValidationError


class alumno(models.Model):
    _name = 'sysnotas.alumno'
    _rec_name = "alum_cui"
    
    alum_cui = fields.Integer(string = "CUI", 
        required = True,
        index = True
        )
    alum_nomb = fields.Char( string = "Nombre", 
        size = 30,
        required = True
        )
    alum_apel = fields.Char( string = "Apellidos", 
        size = 30,
        required = True
        )
    alum_obs = fields.Text(string = "Observacion",
        help = "observaciones al alumno "
        )

    _sql_constraints = [
        ('alum_cui_uniq',
         'UNIQUE (alum_cui)',
         'El CUI no puede repetirse!')]


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
    sql_constraints = [
        ('curs_cod_unique',
         'UNIQUE (curs_cod)',
         'El codigo de curso no puede repetirse!')]


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
    sql_constraints = [
        ('matr_cod_unique',
         'UNIQUE (matr_cod)',
         'El codigo de matricula no puede repetirse!')]

    sql_constraints = [
        ('matr_alum_cui',
         'UNIQUE (matr_alum_cui)',
         'El codigo de alumno no puede repetirse!')]

    @api.one
    @api.depends('matr_alum_cui')
    def make_nombre(self):        
        if self.matr_alum_cui:
            self.matr_alum_mst = self.matr_alum_cui.alum_nomb +" "+ self.matr_alum_cui.alum_apel 

class horario(models.Model):
    _name = 'sysnotas.hrio'
    _rec_name = "hrio_deno"

    hrio_deno = fields.Integer(
        string = "hora",
        required = True,
        index = True,
        help = "ejemplo: 13, 14, 7"
        )

    sql_constraints = [
        ('hrio_deno_unique',
         'UNIQUE (hrio_deno)',
         'Ya existe hora!')]    

class tipohora(models.Model):
    _name = 'sysnotas.tiph'
    _rec_name = 'tiph_deno'

    tiph_deno = fields.Char(
        string = "Siglas",
        required = True,
        size = 2,
        index = True,
        help = "ejemplo: TE, LB, TP "
        )    

    sql_constraints = [
        ('hrio_deno_unique',
         'UNIQUE (hrio_deno)',
         'Ya existe tipo!')] 

class curs_hrio(models.Model):
    _name = 'sysnotas.crsho'
    _rec_name = 'crsho_show'


    crsho_tiph_cod = fields.Many2one(
        'sysnotas.tiph',
        string = 'Tipo'
        )
    crsho_hrio_cod = fields.Many2one(
        'sysnotas.hrio',
        string = 'Horas'
        )

    curs_curs_hrio = fields.Many2one(
        'sysnotas.curso'
        )
    crsho_show = fields.Char(string = "mostrar",        
        compute = 'make_show',
        store = True,
        )

    @api.multi
    @api.depends('crsho_tiph_cod', 'crsho_hrio_cod')
    def make_show(self):        
        if self.crsho_tiph_cod and self.crsho_hrio_cod:
            self.crsho_show = self.crsho_tiph_cod.tiph_deno + str(self.crsho_hrio_cod.hrio_deno)
            print self.crsho_show