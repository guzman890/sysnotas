# -*- coding: utf-8 -*-

from openerp import models, fields, api

class alumno(models.Model):
    _name = 'sysnotas.alumno'
    _rec_name = "alumno_name"
    
    alum_cui = fields.Integer(string = "CUI", 
        required = True,
        index = True
        )
    alum_name = fields.Char( string = "Nombre", 
        size = 30,
        required = True
        )
    alum_obs = fields.Text(string = "Observacion",
        help = "observaciones al alumno "
        )


class curso(models.Model):
    _name = 'sysnotas.curso'
    _rec_name = "curso_name"

    curso_codigo = fields.Integer(string = "Codigo", 
        required = True,
        index = True
        )
    curso_name = fields.Char( string = "Nombre", 
        size = 30,
        required = True
        )
    curso_creditos = fields.Integer(string = "creditos",
        help = "cantidad de creditos "
        )
    curso_matricula_codigo = fields.Many2many(
        'sysnotas.matricula',
        string = 'matr_cod' 
        )


class matricula(models.Model):
    _name = 'sysnotas.matricula'
    _rec_name = "matricula_codigo"

    matricula_codigo = fields.Integer(string = "Codigo",
        help = "codigo de matricula",
        index = True
        )
    matricula_name = fields.Char(string = "Codigo",
        help = "nombre de matricula",
        size = 30
        )
    matricula_alumno_obs = fields.Text(string = "Observacion", 
        store =False,
        compute = 'ObtObs'
        )
    matricula_alumno_cui = fields.Many2one(
        'sysnotas.alumno')

    matricula_curso_codigo = fields.Many2many(
        'sysnotas.curso',
        string = 'curs_cod'
        )
    
    @api.multi
    @api.depends('matricula_alumno_cui')
    def ObtObs(self):
        self.matricula_alumno_obs = self.matricula_alumno_cui.alumno_obs