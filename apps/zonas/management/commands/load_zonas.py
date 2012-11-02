#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import xlrd
from collections import namedtuple

from django.core.management.base import BaseCommand

from apps.zonas import models

def load_catastro(xlsCatastro):
    xlsFileCatastro = xlrd.open_workbook(xlsCatastro)
    hoja = xlsFileCatastro.sheet_by_index(0)
    cols = range(hoja.ncols)
    t_fila = namedtuple("Fila", ", ".join(map(lambda col: hoja.cell(1, col).value, cols)))
    calles = {}
    for n_fila in xrange(2, hoja.nrows):
        fila = t_fila(*map( lambda col: hoja.cell(n_fila, col).value, cols))
        key = (int(fila.Circ), int(fila.Sector))
        calle = calles.setdefault(key, [])
        calle.append({"nombre":fila.Calle.title(), "desde": int(fila.Numero), "hasta": int(fila.Numero)})
    return calles

def load_zonas(xlsZonas):
    xlsFileZonas = xlrd.open_workbook(xlsZonas)
    hoja = xlsFileZonas.sheet_by_index(0)
    cols = range(hoja.ncols)
    t_fila = namedtuple("Fila", ", ".join(map(lambda col: hoja.cell(0, col).value, cols)))
    zonas = []
    for n_fila in xrange(1, hoja.nrows):
        fila = t_fila(*map( lambda col: hoja.cell(n_fila, col).value, cols))
        zona = {}
        zona["numero"] = int(fila.ZONA)
        zona["barrio"] = fila.BARRIOS.title()
        try:
            zona["circ"] = [ int(fila.CIRC) ]
        except:
            zona["circ"] = map(lambda c: int(c), fila.CIRC.split(","))
        try:
            zona["sector"] = [ int(fila.SECTOR) ]
        except:
            zona["sector"] = map(lambda s: int(s), fila.SECTOR.split(","))
        zonas.append(zona)
    return zonas

def mixCatastroZona(catastro, zona):
    catastro["barrio"] = zona["barrio"]
    catastro["zona"] = zona["numero"]
    return catastro
    
class Command(BaseCommand):
    def handle(self, xlsCatastro, xlsZonas, **options):
        comodoro, _ = models.Localidad.objects.get_or_create(nombre = "Comodoro Rivadavia", defaults = {"nombre": "Comodoro Rivadavia"})
        catastro = load_catastro(xlsCatastro)
        for zona in load_zonas(xlsZonas):
            for circ in zona["circ"]:
                for sector in zona["sector"]:
                    catastro[(circ, sector)] = map(lambda c: mixCatastroZona(c, zona), catastro[(circ, sector)])
        for calles in catastro.values():
            for calleAltura in calles:
                if calleAltura["nombre"]:
                    calle, _ = comodoro.calle_set.get_or_create(nombre = calleAltura["nombre"], defaults = {"nombre": calleAltura["nombre"]})
                    calleAltura.pop("nombre")
                    calleAltura["vereda"] = 3
                    altura, _ = calle.altura_set.get_or_create(desde = calleAltura["desde"], hasta = calleAltura["hasta"], defaults = calleAltura)
