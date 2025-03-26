#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QtGlobal>
#include <QTextStream>
#include <QVector>
#include <QtMath>
#include <QElapsedTimer>
#include <QUdpSocket>
#include <QNetworkDatagram>
#include <QDebug>



QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButton_Load_clicked();

    void on_pushButton_Save_clicked();

    void on_pushButton_brightness_clicked();

    void on_verticalSlider_brightness_valueChanged(int value);

    void on_pushButton_contrast_clicked();

    void on_verticalSlider_contrast_valueChanged(int value);

    void update_output();

    void update_input();

private:
    QUdpSocket *udpSocket;
    QString udpServerIP;
    quint16 udpServerPort;
    Ui::MainWindow *ui;
    bool image_not_set=1;
    QImage base_image,output_image;
    QVector<double> histogram;
    int width, height, contrast=99, brightness=0;
    double pixel_scale;
    QElapsedTimer timer;
    void sendUdpMessage();
};
#endif // MAINWINDOW_H
