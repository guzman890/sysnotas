# -*- coding: utf-8 -*-

from openerp import models, fields, api

class alumno(models.Model):
    _name = 'sysnotas.alumno'
    _rec_name = "alum_nomb"
    
    alum_cui = fields.Integer(string = "CUI", 
        required = True,
        index = True
        )
    alum_nomb = fields.Char( string = "Nombre", 
        size = 30,
        required = True
        )
    alum_obs = fields.Text(string = "Observacion",
        help = "observaciones al alumno "
        )


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
    matr_alum_obs = fields.Text(string = "Observacion", 
        store = False,
        compute = 'ObtObs'
        )

    """" relaciones """
    matr_alum_cui = fields.Many2one(
        'sysnotas.alumno')

    matr_curs_cod = fields.Many2many(
        'sysnotas.curso',
        string = 'curs_cod'
        )
    
    @api.multi
    @api.depends('matr_alum_cui')
    def ObtObs(self):
        self.matr_alum_obs = self.matr_alum_cui.alum_obs