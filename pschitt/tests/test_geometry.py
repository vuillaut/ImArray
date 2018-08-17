from pschitt import geometry as geo
import numpy as np


def test_image_point_pfi():
    """
    Test the projection of a point in the image focal plane
    """
    tel = geo.Telescope([0, 0, 0], [0, 0, 1])
    tel.focale = 10
    point = np.array([5, 0, 20])
    assert (geo.image_point_pfi(point, tel) == np.array([-2.5, 0., -10.])).all()


def test_image_point_pfo():
    """
    Test the projection of a point in the object focal plane
    """
    tel = geo.Telescope([0, 0, 0], [0, 0, 1])
    tel.focale = 10
    point = np.array([5, 0, 20])
    assert (geo.image_point_pfo(point, tel) == np.array([-2.5, 0., 10.])).all()

def test_image_shower_pfi():
    """
    Test the projection of a shower in the image focal plane
    """
    shower = np.array([[0, 0, 20], [10, 0, 20]])
    tel = geo.Telescope([10, 0, 0], [0, 0, 1])
    tel.focale= 10
    assert (geo.image_shower_pfi(shower, tel) == np.array([[15., 0., -10], [10, 0, -10]], dtype=float)).all()

def test_image_shower_pfo():
    """
    Test the projection of a shower in the object focal plane
    """
    shower = np.array([[0, 0, 20], [10, 0, 20]])
    tel = geo.Telescope([10, 0, 0], [0, 0, 1])
    tel.focale = 10
    assert (geo.image_shower_pfo(shower, tel) == np.array([[15, 0, 10], [10, 0, 10]], dtype=float)).all()


def test_telescope_display_info():
    """
    Test the display info function in the Telescope class.
    """
    tel = geo.Telescope([0, 0, 0], [0, 0, 1])
    tel.display_info()


def test_is_particle_visible():
    particle_position = np.array([10, 0, 20])
    telescope = geo.Telescope([0, 0, 0], [1, 0, 2])
    particle_direction = np.array([-1, 0, -2])
    particle_energy = 1
    assert geo.is_particle_visible(particle_position, particle_direction, particle_energy, telescope)
